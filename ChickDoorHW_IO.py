import RPi.GPIO as GPIO
import DoorLock
import ChickenPiLogging

#setup of IO
MotorClockWiseControlPort = 38
MotorCounterClockwiseControlPort = 40


def InitializeMotorIO(*args):
    GPIO.setup(MotorClockWiseControlPort, GPIO.OUT)
    GPIO.setup(MotorCounterClockwiseControlPort, GPIO.OUT)
    ChickenPiLogging.LogInfo('Initializing Motor IO')
    TurnMotorOff()

def TurnMotorOff(*args):
    ChickenPiLogging.LogInfo('Motor Off')
    GPIO.output(MotorCounterClockwiseControlPort, GPIO.LOW)
    GPIO.output(MotorClockWiseControlPort, GPIO.LOW)
    DoorLock.LockDoor()


def TMO(*args):
    ChickenPiLogging.LogInfo('Motor Off')
    GPIO.output(MotorCounterClockwiseControlPort, GPIO.LOW)
    GPIO.output(MotorClockWiseControlPort, GPIO.LOW)
    DoorLock.LockDoor()

def TurnMotorClockWise(*args):
    DoorLock.UnlockDoor()
    ChickenPiLogging.LogInfo('Motor On Turning Clockwise')
    GPIO.output(MotorCounterClockwiseControlPort, GPIO.LOW)
    GPIO.output(MotorClockWiseControlPort, GPIO.HIGH)

def TurnMotorCounterClockWise(*args):
    DoorLock.UnlockDoor()
    ChickenPiLogging.LogInfo('Motor On Turning Counter ClockWise')
    GPIO.output(MotorClockWiseControlPort, GPIO.LOW)
    GPIO.output(MotorCounterClockwiseControlPort, GPIO.HIGH)


