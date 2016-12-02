import time
import RPi.GPIO as GPIO
import ChickDoorHW_IO as ChickDoor
import DoorLock


DoorSensorValues = ['DoorOpened','Door Closed', 'Door Partially Opened','Door Status Undetermined' ]


# Setup of Door Open/Close Sensors
DoorClosedSensorPort = 35
DoorOpenedSensorPort = 33

# the time in seconds after the motor is forced to stop because it is running too long
MotorTimeoutTime = 32

def InitializeSensors(*args):
    GPIO.setup(DoorClosedSensorPort, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DoorOpenedSensorPort, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    print('Door Sensors Initialized')
    
def DoorOpened(self):
    print('DoorOpened Procedure Called')
    ChickDoor.TurnMotorOff()
    VerifyDoorStatus(DoorSensorValues[0])
    
def OpenDoor(*args):

    #If door already opened, don't open
    DoorState=GetDoorStatus()
    if DoorState == DoorSensorValues[0]:
        print('Door already opened, ignoring OpenDoor command')
    else:
        print('Opening Door')
        ChickDoor.TurnMotorOff()

        MotorStartTime = time.time()
        ChickDoor.TurnMotorCounterClockWise()

        DoorMovementSuccess = DetermineWhenToStopMotor(DoorOpenedSensorPort,MotorStartTime)

        if DoorMovementSuccess:
            DoorOpened(1)
            print('Time to open door: {0:.2f} seconds'.format(time.time() - MotorStartTime))
        
def DoorClosed(self):
    print('DoorClosed Procedure Called')
    ChickDoor.TurnMotorOff()
    VerifyDoorStatus(DoorSensorValues[1])
       

def CloseDoor(*args):

    #If door already opened, don't open
    DoorState=GetDoorStatus()
    if DoorState == DoorSensorValues[1]:
        print('Door already closed, ignoring CloseDoor command')
    else:
        print('Closing Door')
        ChickDoor.TurnMotorOff()

        MotorStartTime = time.time()
        ChickDoor.TurnMotorClockWise()

        DoorMovementSuccess = DetermineWhenToStopMotor(DoorClosedSensorPort,MotorStartTime)

        if DoorMovementSuccess:
            DoorClosed(1)
            print('Time to close door: {0:.2f} seconds'.format(time.time() - MotorStartTime))


def DetermineWhenToStopMotor(SensorPort,MotorStartTime):
    CurrDoorStatus = GPIO.input(SensorPort)
    while CurrDoorStatus:
        time.sleep(.2)
        if CheckForMotorTimeOut(MotorStartTime) == True:
            print('Motor Running Longer than it should, forcing motor off')
            ChickDoor.TurnMotorOff()
            return(False)
            break
        CurrDoorStatus = GPIO.input(SensorPort)
        if CurrDoorStatus == False:
            print('Debouncing Sensor')
            time.sleep(.2)
            # Start Debounce
            CurrDoorStatus = GPIO.input(SensorPort)
            if CurrDoorStatus == False:
                # Sensor Debounced
                print('Sensor Debounced')
                return(True)
                break

def VerifyDoorStatus(ExpectedDoorStatus):
    ActualDoorStatus = GetDoorStatus()
    if ExpectedDoorStatus == ActualDoorStatus:
        print('Door Status as Expected, Current Door Status = {}'.format(ActualDoorStatus))
    else:
        print('!!!!!! Unexpected Door Status, Current Door Status = {}, Expected Door Status = {} !!!!!'.format(ActualDoorStatus,ExpectedDoorStatus))
    

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

# Below this only for debug
GPIO.setmode(GPIO.BOARD)
DoorLock.InitializeDoorLockIO()
ChickDoor.InitializeMotorIO()
InitializeSensors();
'''

'''


# for loop testing:
for i in range(5):
    OpenDoor()
    CloseDoor()
    print('i = {}'.format(i))

'''
