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
PLAY_ACTION = "PLAY"  # Command for stopping accepting connections and starting a new game


# =========== UI ===========
CLIENT_UI = './PYQTDesignerStuff/ClientUI.ui'


# =========== STYLES ===========
LIGHTBEIGE_BG = "rgb(251, 246, 227)"
BUTTONS = "rgb(245, 189, 76)"
TEXT_BUTTONS = "rgb(251, 246, 227)"
DIS_BUTTONS = "rgb(248, 212, 139)"
FIELDS = "rgb(255, 255, 255)"
LABELS = "rgb(125, 132, 88)"


def set_designs(buttons: [], fields: [], labels: []):
    button_style = f"""
    QPushButton:enabled {{ 
        background-color: {BUTTONS};  
        color: {TEXT_BUTTONS};
    }}
    QPushButton:disabled {{ 
        background-color: {DIS_BUTTONS};  
        color: {TEXT_BUTTONS};
    }}
"""
    field_style = f"background-color: {FIELDS};"
    label_style = f"color: {LABELS}"

    for button in buttons:
        button.setStyleSheet(button_style)
    for field in fields:
        field.setStyleSheet(field_style)
    for label in labels:
        label.setStyleSheet(label_style)



