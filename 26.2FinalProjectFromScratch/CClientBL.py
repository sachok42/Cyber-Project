import socket
from config import *
from protocol import *


class TelnetClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")

            # Read the initial login prompt from the server
            login_prompt = self.client_socket.recv(1024).decode()
            print(login_prompt, end="")  # Display prompt without adding a new line

            # Send login with newline so the server reads it correctly
            login = input()
            self.client_socket.sendall((login + "\n").encode())

        except Exception as e:
            print(f"Error: {e}")
            self.client_socket = None

    '''
    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"Error: {e}")
            self.client_socket = None
        '''

    def send_message(self, message):
        if self.client_socket:
            try:
                self.client_socket.sendall(message.encode())
                response = self.client_socket.recv(1024).decode()
                print(f"Server: {response}")
            except Exception as e:
                print(f"Error: {e}")

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed.")


if __name__ == "__main__":
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    client = TelnetClient(host, port)
    client.connect()

    while True:
        message = input()
        client.send_message(message)
        response = client.client_socket.recv(1024).decode()
        print(f"Server: {response}")
        if message.lower() == 'exit':
            break
    client.close()

'''
if __name__ == "__main__":
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    client = TelnetClient(host, port)
    client.connect()

    while True:
        message = input()
        client.sendall(message.encode())
        message = ""
        while message == "":
            response = client.recv(1024).decode()
            print(f"Server: {response}")
        if message.lower() == 'exit':
            break
    client.close()

'''