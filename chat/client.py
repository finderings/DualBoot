import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345


def receive():
    while True:
        try:
            message = s.recv(1024).decode("utf-8")
            if len(message) == 0:
                s.close()
                print("Connection lost")
                break
            print(message)
        except OSError:
            print("Connection lost")
            break


def send():
    while True:
        try:
            message = input("")
            s.send(bytes(message, "utf-8"))
            if message.lower() == 'quit':
                s.close()
                break
        except OSError:
            print('Connection problems')
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    receive_thread = Thread(target=receive)
    send_thread = Thread(target=send)
    receive_thread.start()
    send_thread.start()
    send_thread.join()
