import RPi.GPIO as GPIO
import time

#setup of IO
DoorLockControlPort = 36
#this port is needed for the Hbrige HW used to drive lock, but always low
DoorLockAlwaysLowControlPort = 32

# delay in seconds before and after of locking and unlock door 
LockDelay=0.5


def InitializeDoorLockIO(*args):
    GPIO.setup(DoorLockControlPort, GPIO.OUT)
    GPIO.setup(DoorLockAlwaysLowControlPort, GPIO.OUT)
    GPIO.output(DoorLockAlwaysLowControlPort, GPIO.LOW)
    print('Initialized Door Lock IO')
    LockDoor()

def UnlockDoor(*args):
    print('Door Unlocked')
    time.sleep(LockDelay)    
    GPIO.output(DoorLockControlPort, GPIO.HIGH)
    time.sleep(LockDelay)    

def LockDoor(*args):
    print('Door Locked')
    time.sleep(LockDelay)    
    GPIO.output(DoorLockControlPort, GPIO.LOW)
    time.sleep(LockDelay)    

'''
# for stand along exec only
GPIO.setmode(GPIO.BOARD)
InitializeDoorLockIO()
'''
