import config, os, sys, requests, socket, logging
from logging.handlers import RotatingFileHandler


extra = {'folder_name': os.path.dirname(os.path.abspath(__file__)).split("/")[-1]}
formatter = logging.Formatter('%(asctime)s - %(levelname)10s - %(folder_name)15s:%(module)15s:%(funcName)30s:%(lineno)5s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
logging.getLogger("requests").setLevel(logging.WARNING)
logger.setLevel(config.LOG_LEVEL)
fileHandler = RotatingFileHandler(config.LOG_FOLDER + '/Applications.log', maxBytes=1024 * 1024 * 1, backupCount=1)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger = logging.LoggerAdapter(logger, extra)

apps = sorted(list(config.application_apps), key=lambda tup: tup[0])
count=0
count_up=0
count_down=0
for name, ip, port, udid in apps:
	try:
		count+=1
		url = config.health_checks_base_url + "/ping/" + udid
		try:
			requests.get(url + "/start")
			status = "up"
			sock = socket.create_connection((ip, port), timeout=10)
			count_up+=1
		except socket.error:
			count_down+=1
			status = "down"
			
		review = "%s (%s:%s) is %s" % (name, ip, port, status)
		logger.info(review)
		requests.get(url if status == "up" else url + "/fail", data=review)
	except:
		pass
review  = "%s Checked (Up: %s, Down: %s)" % (count, count_up, count_down)
logger.info(review)

