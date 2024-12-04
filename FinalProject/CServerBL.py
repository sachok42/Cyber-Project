import socket
import threading
import random
from CProtocol import Protocol, RoleManager
from config import *

# Configuration Variables
HOST = '0.0.0.0'  # Server host address
PORT = 0000  # Server port
BUFFER_SIZE = 1024  # Buffer size for receiving data
MAX_CONNECTIONS = 5  # Maximum number of simultaneous connections


class Server:
    def __init__(self, host=HOST, port=PORT):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(MAX_CONNECTIONS)
        self.protocol = Protocol()
        self.clients = {}
        self.round_active = True
        self.word_list = ["apple", "banana", "cat", "dog", "mountain"]
        self.current_word = random.choice(self.word_list)
        self.role_manager = None

    def start(self):
        print(f"Server started on {HOST}:{PORT}. Waiting for connections...")
        while True:
            client_socket, client_address = self.server.accept()
            print(f"Connection from {client_address}")
            self.clients[client_socket] = 'guesser'
            self.send_message(client_socket, self.protocol.create_message("WELCOME", "Welcome to Charades!"))
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(BUFFER_SIZE).decode('FORMAT')
                command, data = self.protocol.parse_message(message)
                self.process_message(client_socket, command, data)
            except:
                self.disconnect_client(client_socket)
                break

    def process_message(self, client_socket, command, data):
        if command == "GUESS" and self.round_active:
            if data.strip() == self.current_word:
                self.broadcast(f"🎉 {self.clients[client_socket]} guessed the word: {data.strip()}!")
                self.round_active = False
                self.reset_round()



