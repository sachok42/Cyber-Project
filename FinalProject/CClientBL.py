import socket
import threading
from CProtocol import Protocol
from config import *


class Client:
    def __init__(self, host=SERVER_HOST, port=PORT):
        """Initializes the client socket and connects to the server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.protocol = Protocol()
        self.running = True

    def start(self):
        """Starts the client to handle sending and receiving messages."""
        write_to_log(f"[Client] {self.client_socket}Connected to the server at {SERVER_HOST}:{PORT}.")
        threading.Thread(target=self.receive_messages, daemon=True).start()

        while self.running:
            user_input = input("Enter your guess (or type 'exit' to quit): ").strip()
            if user_input.lower() == 'exit':
                self.send_message("EXIT")
                self.running = False
            else:
                self.send_message("GUESS", user_input)

    def send_message(self, command, data=""):
        """Sends a protocol-compliant message to the server."""
        message = self.protocol.create_message(command, data)
        self.client_socket.send(message.encode(FORMAT))

    def receive_messages(self):
        """Continuously receives messages from the server and processes them."""
        while self.running:
            try:
                message = self.client_socket.recv(BUFFER_SIZE).decode(FORMAT)
                command, data = self.protocol.parse_message(message)
                self.process_message(command, data)
            except ConnectionError:
                write_to_log(f'[Client] {self.client_socket} Disconnected from the server.')
                self.running = False
                break

    def process_message(self, command, data):
        """Processes received messages based on their command."""
        if command != "":
            if command in self.protocol.commands:
                self.protocol.commands[command](data)
            else:
                write_to_log(f"Unknown command received: {command}")

if __name__ == "__main__":
    client = Client()
    client.start()
