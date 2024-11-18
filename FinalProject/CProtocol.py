import ipaddress
from datetime import datetime
import socket
import random
import logging


SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "127.0.0.1"
PORT: int = 12345
BUFFER_SIZE: int = 1024
HEADER_LEN: int = 2
FORMAT: str = 'utf-8'
DISCONNECT_MSG: str = "EXIT"


# prepare Log file
LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# screen translation
#parse if screen or text



def write_to_log(msg):
    logging.info(msg)
    print(msg)




