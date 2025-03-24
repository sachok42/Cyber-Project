# =========== NETWORK ===========

SERVER_HOST: str = "127.0.0.1"
PORT: int = 1112
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

# roles
DRAW_ROLE = True
GUESS_ROLE = False


# =========== UI ===========
CLIENT_UI = './PYQTDesignerStuff/ClientUI.ui'


# =========== STYLES ===========
# palette swatches https://coolors.co/f5bd4c-fbf6e3-543e12-ec9146-f4ccc2-7d8458-ffffff-b84169-be5277-c46283
LIGHTBEIGE_BG = "rgb(251, 246, 227)"
BUTTONS = "rgb(245, 189, 76)"
BORDER_BUTTONS = "rgb(236, 145, 70)"
TEXT_BUTTONS = "rgb(251, 246, 227)"
DIS_BUTTONS = "rgb(248, 212, 139)"
DIS_BORDER_BUTTONS = "rgb(243, 189, 144)"  # Fixed typo
FIELDS = "rgb(255, 255, 255)"
LABELS = "rgb(125, 132, 88)"
SHADOW_BUTTONS = "rgb(230, 150, 60)"  # Slightly darker shade for shadow effect
DIS_SHADOW_BUTTONS = "rgb(220, 180, 120)"  # Softer shadow for disabled buttons


def set_designs(buttons: list, fields: list, labels: list):
    button_style = f"""
    QPushButton:enabled {{ 
        background-color: {BUTTONS};  
        color: {TEXT_BUTTONS};
        border: 2px solid {BORDER_BUTTONS};  /* Main border */
        border-bottom: 4px solid {SHADOW_BUTTONS};  /* Simulated shadow at the bottom */
        border-radius: 8px;
    }}
    QPushButton:disabled {{ 
        background-color: {DIS_BUTTONS};  
        color: {TEXT_BUTTONS};
        border: 2px solid {DIS_BORDER_BUTTONS};  /* Softer border for disabled buttons */
        border-bottom: 4px solid {DIS_SHADOW_BUTTONS};  /* Softer shadow for disabled buttons */
        border-radius: 8px;
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



