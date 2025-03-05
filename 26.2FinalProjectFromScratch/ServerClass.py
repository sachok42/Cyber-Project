#!/usr/bin/python
import socket
# import os
from queue import SimpleQueue
from threading import Thread, current_thread
from config import *
from protocol import *

# VARIABLES
users = ('a', 'b')  # List of allowed users
connected = {}  # Dictionary to store connected clients

# Handles initial client login
def gateman(q, connection, address):
    file = connection.makefile(mode='rw', buffering=1)  # Create file object for socket
    file.write('login: ')  # Prompt for login
    file.flush()
    login = file.readline().rstrip()  # Read client input
    q.put(Message('authentication', [connection, address, file, login, current_thread()]))  # Send authentication request to main queue
    return

# Reads incoming messages from client
def clientin(client):
    for word in client.file:
        client.qsuper.put(Message('msg', (client, word.rstrip())))  # Put messages into server queue
    client.qsuper.put(Message('logout', client))  # Notify server of client logout
    return

# Sends outgoing messages to client
def clientout(client):
    client.file.write(f'Welcome\n')  # Welcome message
    client.file.flush()

    while True:
        m = client.qout.get()  # Get message from queue
        if m.action == 'exit':  # Exit command
            client.file.write('Good bye\n')
            break
        elif m.action == 'msg':  # Regular message
            client.file.write(m.data + '\n')
            client.file.flush()
    return

# Main server function
def server(super_queue):
    connected['root'] = Client_connection(None, None, None, 'root')  # Root user placeholder

    while True:
        msg = super_queue.get()  # Get message from queue
        if msg.action == 'connection':
            g = Thread(target=gateman, args=(super_queue, *msg.data))  # Start login thread
            g.start()
        elif msg.action == 'authentication':
            gate_thread = msg.data.pop()
            gate_thread.join()  # Wait for login thread to complete
            allow, args = validate(*msg.data)  # Validate login
            if allow:
                broadcast(connected['root'], f'{args.login} connected from {args.address}')  # Notify clients of connection
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
        elif msg.action == 'logout':
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
        elif msg.action == 'msg':
            broadcast(*msg.data)  # Broadcast message
        else:
            print('Unknown action')  # Debug unknown actions
    return

# Main function to initialize server
def main(argv=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket
    sock.bind((SERVER_HOST, PORT))  # Bind socket to host and port
    sock.listen()  # Start listening for connections

    main_queue = SimpleQueue()  # Main queue for messages
    sup = Thread(target=server, args=(main_queue,))  # Start server thread
    sup.start()

    while True:
        main_queue.put(Message('connection', sock.accept()))  # Accept client connections
    return

if __name__ == "__main__":
    main()

