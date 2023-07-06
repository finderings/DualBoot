import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345
users = {}
addresses = {}


def new_user(connection: socket.socket) -> None:
    name = connection.recv(1024).decode("utf-8")
    while name in users.values():
        error_message = "Name already taken. Please choose another name."
        connection.send(bytes(error_message, "utf-8"))
        name = connection.recv(1024).decode("utf-8")
    welcome = f"Hello {name}! If you want to leave chat enter 'quit'."
    connection.send(bytes(welcome, "utf-8"))
    message = f"{name} join chat"
    send_message(bytes(message, "utf-8"))
    users[connection] = name
    while True:
        try:
            message = connection.recv(1024)
            if not message:
                remove(connection)
                break
            if message.decode("utf-8") != "quit":
                send_message(message, name + ": ", connection)
            else:
                connection.send(bytes("quit", "utf-8"))
                remove(connection)
                break
        except OSError:
            remove(connection)
            break


def remove(connection):
    name = users[connection]
    connection.close()
    del users[connection]
    del addresses[connection]
    send_message(bytes(f"{name} left chat", "utf-8"))
    print(f"{name} left chat")


def send_message(message, name="", connection=None):
    for usr in users:
        if usr != connection:
            usr.send(bytes(name, "utf-8") + message)
    if connection is not None:
        print(f'{addresses[connection][0]} {name}{message.decode("utf-8")}')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, address = s.accept()
        print("%s:%s Join chat" % address)
        conn.send(bytes("Hello! Enter your name", "utf-8"))
        addresses[conn] = address
        Thread(target=new_user, args=(conn,)).start()
