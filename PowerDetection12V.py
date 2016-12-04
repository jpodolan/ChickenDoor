import RPi.GPIO as GPIO
import ChickenPiLogging
import time

#setup of IO
PowerDetectionPort = 32

TwelveVoltPowerActive = True


def Initialize12V_PowerDetection(*args):
    GPIO.setup(PowerDetectionPort, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    ChickenPiLogging.LogInfo('12V Power Detection Initialized ')
    
def Is12V_PowerActive(*args):
    global TwelveVoltPowerActive
    PowerState12V = GPIO.input(PowerDetectionPort)
    if PowerState12V == False:
        if TwelveVoltPowerActive == True:
            ChickenPiLogging.LogCritical('12 Volt Power Loss Detected')
            TwelveVoltPowerActive = False
        return(False)
    else:
        if TwelveVoltPowerActive == False:
            ChickenPiLogging.LogError('12 Volt Power Re-Established')
            TwelveVoltPowerActive = True
        return(True)

'''
# for stand along exec only
GPIO.setmode(GPIO.BOARD)
Initialize12V_PowerDetection()
    
while True:
    Is12V_PowerActive()
    time.sleep(1)
    print('12 V Power Active = {}'.format(TwelveVoltPowerActive))
'''

