import socket
# import os
from queue import SimpleQueue
from threading import Thread, current_thread
from config import *
from protocol import *


class TelnetClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.login = None

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

            # Receive confirmation whether the login is correct and save it if so - may be useful later
            # response = self.client_socket.recv(1024).decode()

            # if response == WELCOME_MSG:
            # self.login = login

        except Exception as e:
            print(f"Error: {e}")
            self.client_socket = None

    # later will be used for creating correct format messages
    def create_message(self, message):
        return message

    def send_message(self, message):
        if self.client_socket:
            try:
                self.client_socket.sendall((self.create_message(message) + "\n").encode())
            except Exception as e:
                print(f"Error: {e}")

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed.")

    # target function for the receiving thread
    def receive_target(self):
        while True:
            msg = self.client_socket.recv(1024).decode()
            print(f"Server: {msg}")

    # target function for the sending thread
    def send_target(self):
        while True:
            msg = input()
            self.send_message(msg)
            if msg.upper() == DISCONNECT_MSG:
                return


if __name__ == "__main__":
    # connect to the server
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    client = TelnetClient(host, port)
    client.connect()

    # start sending and receiving threads
    recv_thread = Thread(target=client.receive_target)
    send_thread = Thread(target=client.send_target)
    recv_thread.start()
    send_thread.start()

    # wait for the sending thread to stop. that happens when the input is disconnect message
    send_thread.join()
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

def connect(self):
    try:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")
    except Exception as e:
        print(f"Error: {e}")
        self.client_socket = None
    '''
