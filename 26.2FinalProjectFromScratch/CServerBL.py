#!/usr/bin/python
import socket
import os
from queue import SimpleQueue
from threading import Thread, current_thread
from config import *
from protocol import *


class Message():
    def __init__(self, action, data=None):
        print('Message', action, data)
        self.action = action
        self.data = data
        return


class Client():
    def __init__(self, connection, address, file, login):
        self.connection = connection
        self.address = address
        self.file = file
        self.login = login
        self.qin = SimpleQueue()
        self.qout = SimpleQueue()
        return


users = ('a', 'b')
connected = {}


def gateman(q, connection, address):
    file = connection.makefile(mode='rw', buffering=1)
    file.write('login: ')
    file.flush()
    login = file.readline().rstrip()
    # file.write('password: ')
    # password = file.readline().rstrip()
    q.put(Message('authentication', [connection, address, file, login, current_thread()]))
    return


def clientin(client):
    for word in client.file:
        client.qsuper.put(Message('msg', (client, word.rstrip())))
    client.qsuper.put(Message('logout', client))
    return


def clientout(client):
    client.file.write('Welcome\n')
    client.file.flush()

    while True:
        m = client.qout.get()
        if m.action == 'exit':
            client.file.write('Good bye\n')
            break
        elif m.action == 'msg':
            client.file.write(m.data + '\n')
            client.file.flush()
    return


def validate(connection, address, file, login):
    if not login in users:
        write_to_log(f'debug def_validate - login {login} not in users {users}') # DEBUG
        return False, 'Permission denied'
    if login in connected:
        write_to_log(f'debug def_validate - login {login} Already logged in from {connected[login].address}')  # DEBUG
        return False, f'Already logged in from {connected[login].address}'
    return True, Client(connection, address, file, login)


def broadcast(client, word):
    word = client.login + ': ' + word
    for c in connected.values():
        if not (c is client or c.login == 'root'):
            c.qout.put(Message('msg', word))
    return


def server(super_queue):
    connected['root'] = Client(None, None, None, 'root')

    while True:
        msg = super_queue.get()
        if msg.action == 'connection':
            g = Thread(target=gateman, args=(super_queue, *msg.data))
            g.start()
        elif msg.action == 'authentication':
            write_to_log("Authentication message received.")  # DEBUG
            gate_thread = msg.data.pop()
            gate_thread.join()
            write_to_log(f"Authenticating user: {msg.data[3]}")  # DEBUG

            allow, args = validate(*msg.data)
            write_to_log(f"debug - allow args: {allow, args}")  # DEBUG
            if allow:
                write_to_log(f"debug - allow/allowed")  # DEBUG
                broadcast(connected['root'], f'{args.login} connected from {args.address}')
                write_to_log(f"debug - broadcasted")  # DEBUG
                args.qsuper = super_queue
                args.ci = Thread(target=clientin, args=(args,))
                args.co = Thread(target=clientout, args=(args,))
                args.ci.start()
                args.co.start()
                connected[args.login] = args
            else:
                write_to_log(f"debug - allow/else")  # DEBUG
                connection, address, file, _ = msg.data
                file.write(args + '\n')
                file.flush()
                file.close()
                connection.shutdown(socket.SHUT_WR)
                connection.close()
        elif msg.action == 'logout':
            broadcast(connected['root'], f'{msg.data.login} left')
            msg.data.qout.put(Message('exit'))
            msg.data.ci.join()
            msg.data.co.join()
            try:
                msg.data.file.flush()
                msg.data.file.close()
                msg.data.connection.shutdown(socket.SHUT_WR)
                msg.data.connection.close()
            except:
                pass
            del connected[msg.data.login]
        elif msg.action == 'msg':
            broadcast(*msg.data)

        else:
            print('Unknown action')
    return


def main(argv=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_HOST, PORT))
    sock.listen()

    super_queue = SimpleQueue()
    sup = Thread(target=server, args=(super_queue,))
    sup.start()

    while True:
        super_queue.put(Message('connection', sock.accept()))

    return


if __name__ == "__main__":
    main()
