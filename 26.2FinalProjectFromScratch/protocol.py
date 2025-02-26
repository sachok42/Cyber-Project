# =========== LOGGING ===========
import logging

LOG_FILE = 'LOG.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)


def write_to_log(msg):
    logging.info(msg)
    print(msg)



