# =========== FERNET ===========

from cryptography.fernet import Fernet
# Encryption Key (Ensure this key is kept secure)
FERNET_KEY = Fernet.generate_key()  # You can save this key and reload it later

DEFAULT_ROLES = ["artist", "guesser"]  # Default roles in the game
MESSAGE_DELIMITER = ":"  # Delimiter for separating command and data

# =========== NETWORK ===========

SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "127.0.0.1"
PORT: int = 12345
BUFFER_SIZE: int = 1024
HEADER_LEN: int = 2
FORMAT: str = 'utf-8'
DISCONNECT_MSG: str = "EXIT"

# =========== COMMANDS ===========
COMMAND_ROLE = "ROLE"  # Command for assigning roles
COMMAND_WORD = "WORD"  # Command for sending the drawing word
COMMAND_GUESS = "GUESS"  # Command for submitting a guess
COMMAND_EXIT = "EXIT"  # Command for exiting the game
COMMAND_WELCOME = "WELCOME"  # Command for welcoming new players

# =========== LOGGING ===========
LOG_FILE = 'LOG.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# =========== WORDS ===========
words_bank = "words.txt"

# =========== DATABASE ===========
DB_FILE = 'charades.db'
POINTS_FOR_CORRECT_GUESS = 10
POINTS_FOR_ARTIST_SUCCESS = 5



