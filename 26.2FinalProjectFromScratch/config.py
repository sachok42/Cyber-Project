# =========== NETWORK ===========

SERVER_HOST: str = "127.0.0.1"
PORT: int = 1114
BUFFER_SIZE: int = 1024
HEADER: str = "04d"
FORMAT: str = 'utf-8'
DISCONNECT_MSG: str = "EXIT"
WELCOME_MSG: str = "Welcome"
MAX_CONNECTIONS: int = 5  # maximal number of players

# =========== ACTIONS ===========
# general
EXIT_ACTION = "EXIT"  # Command for exiting the game
WELCOME_ACTION = "WELCOME"  # Command for welcoming new players
CONNECTION_ACTION = "CONNECTION"
AUTHENTICATION_ACTION = "AUTHENTICATION"
TEXT_ACTION = "TEXT"  # REGULAR TEXT MESSAGE TO BE BROADCASTED
LOGOUT_ACTION = "LOGOUT"
# gameplay
ROLE_ACTION = "ROLE"  # Command for assigning roles
WORD_ACTON = "WORD"  # Command for sending the drawing word
GUESS_ACTION = "GUESS"  # Command for submitting a guess
PLAY_ACTION= "PLAY"  # Command for stopping accepting connections and starting a new game
