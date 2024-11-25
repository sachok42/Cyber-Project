import ipaddress
from datetime import datetime
import socket
import random
import logging
import random


SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "127.0.0.1"
PORT: int = 12345
BUFFER_SIZE: int = 1024
HEADER_LEN: int = 2
FORMAT: str = 'utf-8'
DISCONNECT_MSG: str = "EXIT"

words_bank = "words.txt"


# prepare Log file
LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# sending:
# screen translation

#receiving:
#parse if screen or text


# word generator
def get_random_word(file_path):
    # Open the file and read the words.txt into a list
    with open(file_path, "r") as file:
        words = file.read().splitlines()

    # Return a random word from the list
    return random.choice(words)


def write_to_log(msg):
    logging.info(msg)
    print(msg)




