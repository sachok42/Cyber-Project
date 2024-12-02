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

# flags
norm_flag = 0
art_flag = 1

words_bank = "words.txt"


# prepare Log file
LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def write_to_log(msg):
    logging.info(msg)
    print(msg)


# choosing a random user to be drawing
def choose_artist(client_handlers: []):
    artist = random.choice(client_handlers)
    artist.make_artist()
    write_to_log(f"[PROTOCOL] Client's became  an artist{artist.client_socket}{artist.address} ")


def undo_allusers(client_handlers: []):
    for c in client_handlers:
        c.undo_artist()
    write_to_log(f"[PROTOCOL] all clients' flags are  set to default")

# word generator
def get_random_word(file_path):
    # Open the file and read the words.txt into a list
    with open(file_path, "r") as file:
        words = file.read().splitlines()

    # Return a random word from the list
    return random.choice(words)



# sending:
# screen translation
def send_big_image(self, my_socket: socket, file_name: str, chunk_size=1024) -> str:
    txt = ''
    try:
        # open file in binary reading mode
        with open(file_name, "rb") as file:
            while True:
                # read by chunk sized bytes
                image_data = file.read(chunk_size)
                # when everything is read
                if not image_data:
                    break  # Reached th end of the file

                my_socket.send(image_data)

            txt = f'Send photo {file_name} - done'
    except FileNotFoundError:
        txt = f'Send photo {file_name} - Photo file doesnt exist'

    return txt

#receiving:
#parse if screen or text






