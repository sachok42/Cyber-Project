import logging
from queue import SimpleQueue

# =========== LOGGING ===========
LOG_FILE = 'LOG.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)


def write_to_log(msg):
    logging.info(msg)
    print(msg)


# Message object to encapsulate action and data
class Message:
    def __init__(self, action, data=None):
        self.action = action  # Action type (e.g., authentication, msg, logout)
        self.data = data  # Additional data
        return
