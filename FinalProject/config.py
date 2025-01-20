# =========== LOGGING ===========
import logging

LOG_FILE = 'LOG.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)


def write_to_log(msg):
    logging.info(msg)
    print(msg)

# =========== FERNET ===========

from cryptography.fernet import Fernet
# Encryption Key (Ensure this key is kept secure)
FERNET_KEY = Fernet.generate_key()  # You can save this key and reload it later

DEFAULT_ROLES = ["artist", "guesser"]  # Default roles in the game
MESSAGE_DELIMITER = ":"  # Delimiter for separating command and data

#mine
DEFROLE = "guesser"
ARTROLE = "artist"

# =========== NETWORK ===========

SERVER_HOST: str = "127.0.0.1"
PORT: int = 12345
BUFFER_SIZE: int = 1024
HEADER: str = "04d"
FORMAT: str = 'utf-8'
DISCONNECT_MSG: str = "EXIT"
MAX_CONNECTIONS: int = 5  # maximal number of players

# =========== COMMANDS ===========
COMMAND_ROLE = "ROLE"  # Command for assigning roles
COMMAND_WORD = "WORD"  # Command for sending the drawing word
COMMAND_GUESS = "GUESS"  # Command for submitting a guess
COMMAND_EXIT = "EXIT"  # Command for exiting the game
COMMAND_WELCOME = "WELCOME"  # Command for welcoming new players
COMMAND_PLAY = "PLAY"  # Command for stopping accepting connections and starting a new game


# =========== WORDS ===========
words_bank = "words.txt"

# =========== DATABASE ===========
DB_FILE = 'charades.db'
POINTS_FOR_CORRECT_GUESS = 10
POINTS_FOR_ARTIST_SUCCESS = 5



