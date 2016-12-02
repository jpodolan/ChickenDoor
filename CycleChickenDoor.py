import time
import RPi.GPIO as GPIO
import ChickDoorHW_IO as ChickDoor

'''
#definition of enums
from enum import Enum
class DoorStatusEnum(Enum):
    DoorStatusUnknown = 0
    DoorClosed = 1
    DoorOpened = 2
    DoorOpening = 3
    DoorClosing = 4
    DoorFault = 5



#not used yet
class DoorSensorEnum(Enum):
    DoorOpened = 0
    DoorClosed = 1
    DoorNotClosed = 2
    DoorNotOpened = 3
'''

# Setup of Door Open/Close Sensors
DoorClosedSensorPort = 35
DoorOpenedSensorPort = 33

def InitializeSensors(*args):
    GPIO.setup(DoorClosedSensorPort, GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(DoorOpenedSensorPort, GPIO.IN,GPIO.PUD_UP)
    
def DoorOpened(OpeningDoor):
    GPIO.remove_event_detect(DoorOpenedSensorPort)
    print('Door Opened')
    ChickDoor.TurnMotorOff()
    
def OpenDoor(*args):
    ChickDoor.TurnMotorOff()
    ChickDoor.TurnMotorCounterClockWise()
    GPIO.add_event_detect(DoorOpenedSensorPort, GPIO.FALLING, callback=DoorOpened, bouncetime=500)
    print('Opening Door')

def DoorClosed(self):
    print('DoorClosed')
    GPIO.remove_event_detect(DoorClosedSensorPort)
    ChickDoor.TurnMotorOff()
    
def CloseDoor(*args):
    print('Closing Door')
    ChickDoor.TurnMotorOff()
    ChickDoor.TurnMotorClockWise()
    GPIO.add_event_detect(DoorClosedSensorPort, GPIO.FALLING, callback=DoorClosed, bouncetime=500)
    print('Closing Door')

def GetDoorStatus(*args):
    DoorOpenedSensor = GPIO.input(DoorOpenedSensorPort)
    DoorClosedSensor = GPIO.input(DoorOpenedSensorPort)
    print('\n===================')
    print('Current Door Status:')
    print(str(MotorStatus))
    print(str(DoorStatus))
    print('Door Opened Sensor = {}' .format(str(DoorOpenedSensor)))
    print('Door Closed Sensor = {}' .format(str(DoorClosedSensor)))
    print('===================\n')

    


# Configure IO
#GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
ChickDoor.InitializeMotorIO()
InitializeSensors();

#initialize Motor
ChickDoor.TurnMotorOff();

while True:
    OpenDoor()
    while GPIO.input(DoorOpenedSensorPort)==True:
        print('Open Door Sleep')
        time.sleep(1)
    CloseDoor()
    while GPIO.input(DoorClosedSensorPort)==True:
        print('Close Door Sleep')
        time.sleep(1)

#GPIO.cleanup()
print('Done')

