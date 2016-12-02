import pdb
import time
import RPi.GPIO as GPIO
#import ChickenDoorControl
import ChickenDoorControlByPolling as ChickenDoorControl
import ChickDoorHW_IO as ChickDoorMotor
import DoorLock

# door open and close times, must be in 24 hour format    
OpenDoorHour = 6
OpenDoorMinute = 00

CloseDoorHour = 17
CloseDoorMinute = 00


# interval in seconds for main loop, must be no greater than 60
TimeInterval=60

DoorOpenedAlreadyToday=False
DoorClosedAlreadyToday=False

#setup HW
GPIO.setmode(GPIO.BOARD)
DoorLock.InitializeDoorLockIO()
ChickDoorMotor.InitializeMotorIO()
ChickenDoorControl.InitializeSensors();


while True:
    CurrentTime = time.localtime()
    
    print('Current Time: {}:{}:{}'.format(CurrentTime.tm_hour, CurrentTime.tm_min,CurrentTime.tm_sec))

    #Reset Flags if New Day
    if CurrentTime.tm_hour == 0 and CurrentTime.tm_min == 0:
        print('Reseting DoorOpenedAlready and DoorClosedAlready Flags')
        DoorOpenedAlreadyToday=False
        DoorClosedAlreadyToday=False

    #Check if time to open door
    if (CurrentTime.tm_hour == OpenDoorHour and CurrentTime.tm_min== OpenDoorMinute) and DoorOpenedAlreadyToday == False:
        print('Time to open door')
        ChickenDoorControl.OpenDoor()
        DoorOpenedAlreadyToday = True;

    #Check if time to close door
    if (CurrentTime.tm_hour == CloseDoorHour and CurrentTime.tm_min == CloseDoorMinute) and DoorClosedAlreadyToday == False:
        print('Time to close door')
        ChickenDoorControl.CloseDoor()
        DoorClosedAlreadyToday = True
        
    time.sleep(TimeInterval)

    

    
#        pdb.set_trace()


'''
#Figure out on startup if the door should be opened or closed
DoorStatus = ChickenDoorControl.GetDoorStatus()
CurrentTime = time.localtime()

print('Door Stautus = {}'.format(DoorStatus))

if DoorStatus == ChickenDoorControl[0]:
    # Door opened
    # if it shouldnt be opened, then close it
    if (CurrentTime.tm_hour > CloseDoorHour) or (CurrentTime.tm_hour ==  CloseDoorHour and CurrentTime.tm_min >= CloseDoorMinute) or :
        ChickenDoorControl.CloseDoor()
        print('Program Startup, Door is opened and it shouldnt be....closing door')
    
if DoorStatus == ChickenDoorControl.[0]:
    # Door closed
    # if it shouldnt be close, then close it
'''
