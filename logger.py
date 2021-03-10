import logging, configparser
from systemd.journal import JournaldLogHandler

config = configparser.ConfigParser()
config.read('wxconf.ini')
log_level = config['log_level']
def log(message, level="info"):
    # get an instance of the logger object this module will use
    logger = logging.getLogger(__name__)
    # instantiate the JournaldLogHandler to hook into systemd
    journald_handler = JournaldLogHandler()
    # set a formatter to include the level name
    journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    # add the journald handler to the current logger
    logger.addHandler(journald_handler)
    if level == "info" and log_level == "info":
        logger.info(message)
    elif level == "debug" and log_level == "debug":
        logger.debug(message)
    elif level == "error" and log_level == "error":
        logger.error(message)
    elif level == "warn" and log_level == "warn":
        logging.warn(message)
    elif level == "critical" and log_level == "critical":
        logging.critical(message)