import time
import RPi.GPIO as GPIO
import ChickDoorHW_IO as ChickDoor
import DoorLock
import PowerDetection12V
import ChickenPiLogging



DoorSensorValues = ['DoorOpened','Door Closed', 'Door Partially Opened','Door Status Undetermined' ]


# Setup of Door Open/Close Sensors
DoorClosedSensorPort = 35
DoorOpenedSensorPort = 33

# the time in seconds after the motor is forced to stop because it is running too long
MotorTimeoutTime = 32

def InitializeSensors(*args):
    GPIO.setup(DoorClosedSensorPort, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DoorOpenedSensorPort, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    ChickenPiLogging.LogInfo('Door Sensors Initialized')
    
def DoorOpened(self):
    ChickenPiLogging.LogInfo('DoorOpened Procedure Called')
    ChickDoor.TurnMotorOff()
    VerifyDoorStatus(DoorSensorValues[0])
    
def OpenDoor(*args):

    #If door already opened, don't open
    DoorState=GetDoorStatus()
    if DoorState == DoorSensorValues[0]:
        ChickenPiLogging.LogError('Door already opened. Ignoring OpenDoor command')
    else:
        ChickenPiLogging.LogInfo('Opening Door')
        ChickDoor.TurnMotorOff()

        MotorStartTime = time.time()
        ChickDoor.TurnMotorCounterClockWise()

        DoorMovementSuccess = DetermineWhenToStopMotor(DoorOpenedSensorPort,MotorStartTime)

        if DoorMovementSuccess:
            DoorOpened(1)
            ChickenPiLogging.LogInfo('Time to open door: {0:.2f} seconds'.format(time.time() - MotorStartTime))
        
def DoorClosed(self):
    ChickenPiLogging.LogInfo('DoorClosed Procedure Called')
    ChickDoor.TurnMotorOff()
    VerifyDoorStatus(DoorSensorValues[1])
       

def CloseDoor(*args):

    #If door already opened, don't open
    DoorState=GetDoorStatus()
    if DoorState == DoorSensorValues[1]:
        ChickenPiLogging.LogError('Door already closed. Ignoring CloseDoor command')
    else:
        ChickenPiLogging.LogInfo('Closing Door')
        ChickDoor.TurnMotorOff()

        MotorStartTime = time.time()
        ChickDoor.TurnMotorClockWise()

        DoorMovementSuccess = DetermineWhenToStopMotor(DoorClosedSensorPort,MotorStartTime)

        if DoorMovementSuccess:
            DoorClosed(1)
            ChickenPiLogging.LogInfo('Time to close door: {0:.2f} seconds'.format(time.time() - MotorStartTime))


def DetermineWhenToStopMotor(SensorPort,MotorStartTime):
    CurrDoorStatus = GPIO.input(SensorPort)
    while CurrDoorStatus:
        time.sleep(.2)
        if CheckForMotorTimeOut(MotorStartTime) == True:
            ChickenPiLogging.LogCritical('Motor Running Longer than it should! Forcing motor off')
            ChickDoor.TurnMotorOff()
            return(False)
            break
        CurrDoorStatus = GPIO.input(SensorPort)
        if CurrDoorStatus == False:
            ChickenPiLogging.LogInfo('Debouncing Sensor')
            time.sleep(.2)
            # Start Debounce
            CurrDoorStatus = GPIO.input(SensorPort)
            if CurrDoorStatus == False:
                # Sensor Debounced
                ChickenPiLogging.LogInfo('Sensor Debounced')
                return(True)
                break

def VerifyDoorStatus(ExpectedDoorStatus):
    ActualDoorStatus = GetDoorStatus()
    if ExpectedDoorStatus == ActualDoorStatus:
        ChickenPiLogging.LogInfo('Door Status as Expected. Current Door Status = {}'.format(ActualDoorStatus))
    else:
        ChickenPiLogging.LogCritical('!!!!!! Unexpected Door Status. Current Door Status = {}. Expected Door Status = {} !!!!!'.format(ActualDoorStatus,ExpectedDoorStatus))
    

def GetDoorStatus(*args):
    DoorOpenedSensor = GPIO.input(DoorOpenedSensorPort)
    DoorClosedSensor = GPIO.input(DoorClosedSensorPort)

    if DoorOpenedSensor == False and DoorClosedSensor == True:
        #Door Opened
        return(DoorSensorValues[0])
    
    if DoorOpenedSensor == True and DoorClosedSensor == False:
        #Door Closed
        return(DoorSensorValues[1])

    if DoorOpenedSensor == True and DoorClosedSensor == True:
        #Door Partially Opened
        return(DoorSensorValues[2])


    if DoorOpenedSensor == False and DoorClosedSensor == False:
        #DoorOpened sensor=Opened and DoorClosedSensor=Closed which is impossible...some error occurred
        return(DoorSensorValues[3])

def CheckForMotorTimeOut(MotorStartTime):
    CurrentTime = time.time()
    if CurrentTime - MotorStartTime >= MotorTimeoutTime:
        #motor timeout 
        return(True)
    else:
        return(False)

'''
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
ChickenPiLogging.SetupLogging()
PowerDetection12V.Initialize12V_PowerDetection()
DoorLock.InitializeDoorLockIO()
ChickDoor.InitializeMotorIO()
InitializeSensors()



# Below this only for debug




# for loop testing:
for i in range(5):
    OpenDoor()
    CloseDoor()
    ChickenPiLogging.LogInfo('i = {}'.format(i))

'''
