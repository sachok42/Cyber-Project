#!/usr/bin/python
import socket
# import os
from queue import SimpleQueue
from threading import Thread, current_thread
from config import *
from protocol import *

# VARIABLES
users = ('a', 'b')  # List of allowed users
connected = {}  # {login: (Client_connection, role)}


# Message object to encapsulate action and data
class Message:
    def __init__(self, action, data=None):
        self.action = action  # Action type (e.g., authentication, msg, logout)
        self.data = data  # Additional data
        return


# Class to handle client connections
class ClientConnection:
    def __init__(self, connection, address, file, login):
        self.connection = connection  # Client socket
        self.address = address  # Client address
        self.file = file  # File object for socket communication
        self.login = login  # Client login name
        self.qin = SimpleQueue()  # Queue for incoming messages
        self.qout = SimpleQueue()  # Queue for outgoing messages
        return


# Handles initial client login
def gateman(q, connection, address):
    file = connection.makefile(mode='rw', buffering=1)  # Create file object for socket
    file.write('login: ')  # Prompt for login
    file.flush()
    login = file.readline().rstrip()  # Read client input
    q.put(Message(AUTHENTICATION_ACTION, [connection, address, file, login, current_thread()]))
    # Send authentication request to main queue
    return


# Reads incoming messages from client and puts them into the server's queue
def clientin(client):
    for word in client.file:
        client.qsuper.put(Message(TEXT_ACTION, (client, word.rstrip())))  # Put messages into server queue
    client.qsuper.put(Message(LOGOUT_ACTION, client))  # Notify server of client logout
    return


# Sends outgoing messages to client
def clientout(client):
    client.file.write(f'Welcome\n')  # Welcome message
    client.file.flush()

    while True:
        m = client.qout.get()  # Get message from queue
        if m.action == EXIT_ACTION:  # Exit command
            client.file.write('Good bye\n')
            break
        elif m.action == TEXT_ACTION:  # Regular message
            client.file.write(m.data + '\n')
            client.file.flush()
    return


# Validates client credentials
def validate(connection, address, file, login):
    if login not in users:
        return False, 'Permission denied'  # Reject if login not in users
    if login in connected:
        return False, f'Already logged in from {connected[login][0].address}'  # Reject if user already connected
    return True, ClientConnection(connection, address, file, login)  # Accept login


# Broadcasts message to all connected clients (except sender and root)
def broadcast(client, word):
    word = client.login + ': ' + word
    for c in connected.values():
        if not (c[0] is client or c[0].login == 'root'):
            c[0].qout.put(Message(TEXT_ACTION, word))  # Add message to client's outgoing queue
    return


# Main server function
def server(super_queue):
    connected['root'] = (ClientConnection(None, None, None, 'root'), None)  # Root user placeholder
    write_to_log(f'[server] - is running')
    while True:
        msg = super_queue.get()  # Get message from queue
        if msg.action == CONNECTION_ACTION:
            g = Thread(target=gateman, args=(super_queue, *msg.data))  # Start login thread
            g.start()
        elif msg.action == AUTHENTICATION_ACTION:
            gate_thread = msg.data.pop()
            gate_thread.join()  # Wait for login thread to complete
            allow, args = validate(*msg.data)  # Validate login
            if allow:
                # Notify clients of connection
                broadcast(connected['root'], f'{args.login} connected from {args.address}')
                args.qsuper = super_queue
                args.ci = Thread(target=clientin, args=(args,))  # Start input thread
                args.co = Thread(target=clientout, args=(args,))  # Start output thread
                args.ci.start()
                args.co.start()
                connected[args.login] = args  # Add client to connected list
            else:
                connection, address, file, _ = msg.data
                file.write(args + '\n')  # Send error message to client
                file.flush()
                file.close()
                connection.shutdown(socket.SHUT_WR)
                connection.close()
        elif msg.action == LOGOUT_ACTION:
            broadcast(connected['root'], f'{msg.data.login} left')  # Notify clients of logout
            msg.data.qout.put(Message('exit'))  # Send exit message
            msg.data.ci.join()
            msg.data.co.join()
            try:
                msg.data.file.close()
                msg.data.connection.shutdown(socket.SHUT_WR)
                msg.data.connection.close()
            except:
                pass
            del connected[msg.data.login]  # Remove client from connected list
        elif msg.action == TEXT_ACTION:
            broadcast(*msg.data)  # Broadcast message
        else:
            print('Unknown action')  # Debug unknown actions
    return


# Main function to initialize server
def main(argv=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket
    sock.bind((SERVER_HOST, PORT))  # Bind socket to host and port
    sock.listen()  # Start listening for connections
    write_to_log(f'[server] - is listening on {SERVER_HOST}{PORT}')

    main_queue = SimpleQueue()  # Main queue for messages
    sup = Thread(target=server, args=(main_queue,))  # Start server thread
    sup.start()

    while True:
        main_queue.put(Message(CONNECTION_ACTION, sock.accept()))  # Accept client connections
    return


if __name__ == "__main__":
    main()
