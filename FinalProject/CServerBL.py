import socket
import threading
import random
from CProtocol import Protocol, RoleManager
import CProtocol
from config import *


class Server:
    def __init__(self, host=SERVER_HOST, port=PORT):
        self._host = host
        self._port = port
        self.protocol = Protocol()
        self.clients = {}
        self.round_active = True
        self.role_manager = None

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self._host, self._port))
        self.server.listen(MAX_CONNECTIONS)
        write_to_log(f"[Server] - started on {SERVER_HOST}:{PORT}. Waiting for connections...")
        while True:
            client_socket, client_address = self.server.accept()
            write_to_log(f"[Server] - Connection from {client_address}")
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
        current_word = random.choice(words_bank)
        if command == "GUESS" and self.round_active:
            if data.strip() == self.current_word:
                self.broadcast(f"🎉 {self.clients[client_socket]} guessed the word: {data.strip()}!")
                self.round_active = False
                self.reset_round()


if __name__ == "__main__":
    server = Server()
    server.start()
