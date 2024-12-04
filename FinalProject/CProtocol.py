import random
import logging
from config import *
import sqlite3


logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)


def write_to_log(msg):
    logging.info(msg)
    print(msg)


class Protocol:
    """Handles message construction and parsing based on the protocol."""

    def __init__(self):
        self.commands = {
            COMMAND_ROLE: self.handle_role,
            COMMAND_WORD: self.handle_word,
            COMMAND_GUESS: self.handle_guess,
            COMMAND_EXIT: self.handle_exit,
            COMMAND_WELCOME: self.handle_welcome
        }

    def create_message(self, command, data=""):
        """Creates a protocol-compliant message."""
        return f"{command}{MESSAGE_DELIMITER}{data}"

    def parse_message(self, message):
        """Parses a protocol message into a (command, data) tuple."""
        try:
            command, data = message.split(MESSAGE_DELIMITER, 1)
        except ValueError:
            command, data = message, ""
        return command, data

    def handle_role(self, data):
        print(f"Your role is: {data}")

    def handle_word(self, data):
        print(f"Your word to draw: {data}")

    def handle_guess(self, data):
        print(f"Guess received: {data}")

    def handle_exit(self, data):
        print("Client exited.")

    def handle_welcome(self, data):
        print(data)

    @staticmethod
    def create_tables():
        """Initializes the database tables."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                score INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def add_user(username):
        """Adds a new user with an initial score."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # User already exists
        finally:
            conn.close()

    @staticmethod
    def get_score(username):
        """Retrieves the user's current score."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT score FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    @staticmethod
    def update_score(username, score):
        """Updates the user's score."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET score = ? WHERE username = ?', (score, username))
        conn.commit()
        conn.close()

    @staticmethod
    def handle_correct_guess(player_name, artist_name):
        """Handles the logic when a player guesses correctly."""
        guesser_score = Protocol.get_score(player_name) + POINTS_FOR_CORRECT_GUESS
        artist_score = Protocol.get_score(artist_name) + POINTS_FOR_ARTIST_SUCCESS

        Protocol.update_score(player_name, guesser_score)
        Protocol.update_score(artist_name, artist_score)

        return {
            "guesser": {"name": player_name, "score": guesser_score},
            "artist": {"name": artist_name, "score": artist_score}
        }


class RoleManager:
    """Manages player roles in the game."""

    def __init__(self, clients, roles=DEFAULT_ROLES):
        self.clients = clients
        self.roles = {}
        self.available_roles = roles

    def assign_roles(self):
        """Assigns roles to clients."""
        self.roles = {client: 'guesser' for client in self.clients}
        artist = random.choice(list(self.clients))
        self.roles[artist] = 'artist'
        return self.roles, artist

    def get_role(self, client):
        """Returns the role of a given client."""
        return self.roles.get(client, 'guesser')

    def broadcast_roles(self):
        """Sends role information to all clients."""
        for client in self.clients:
            role_message = f"{COMMAND_ROLE}{MESSAGE_DELIMITER}{self.roles[client]}"
            client.send(role_message.encode('FORMAT'))




