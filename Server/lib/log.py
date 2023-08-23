#importing module
import logging, datetime, os

date = datetime.datetime.now()
logFolder = "./logs/"
logName = str(date.year) + str(date.month) + str(date.day) + ".log"


try:
	os.stat(logFolder)
except:
	os.mkdir(logFolder)

#Create and configure logger
logging.basicConfig(filename=logFolder + logName,
                    format='%(asctime)s %(message)s',
                    filemode='w')

#Creating an object
logger=logging.getLogger()

#Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

def log(msg, level):
	# log to file but also print to console
	if level == "debug":
		logger.debug(msg)
	elif level == "info":
		logger.info(msg)
	elif level == "warning":
		logger.warning(msg)
	elif level == "error":
		logger.error(msg)
	elif level == "critical":
		logger.critical(msg)

	print(msg)
