import logging
import time

path = '/mnt/PodolanServer/LogFiles/'
filename = 'ChickenPieLog.csv'

def SetupLogging():
    global logger
    logger = logging.getLogger('ChickPieCoop')
    logger.setLevel(logging.DEBUG)

    #setup path and file name of logging files
    CurrentTime = time.localtime()
    file = str(CurrentTime.tm_year) + str(CurrentTime.tm_mon) + str(CurrentTime.tm_mday) + ' '
    file = file + str(CurrentTime.tm_hour) + str(CurrentTime.tm_min) + str(CurrentTime.tm_sec) + ' '
    file = file + filename
    pathfile = path + file
    hdlr = logging.FileHandler(pathfile)
    logger.addHandler(hdlr)

    #Add column headers to file
    logger.info('Date,Time,Type,Message')

    #Define prefix for each log entry
    formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s','%m/%d/%Y,%H:%M:%S')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    # first log entry
    logger.info('Logging Started')


def LogInfo(msg):
    logger.info(msg)
    print(msg)

def LogWarning(msg):
    logger.warning(msg)
    print(msg)

def LogError(msg):
    logger.error(msg)
    print(msg)

def LogCritical(msg):
    logger.critical(msg)
    print(msg)