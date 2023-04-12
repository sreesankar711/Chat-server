from socket import *
import threading
import sys


def receive_messages(cSocket):
    while True:
        message = cSocket.recv(1024).decode()
        if not message:
            break
        if ':' not in message:
            print(f"\r\033[K{message}\n{name}: ", end="")
            if name in message:
                print("\r\033[K", end="")
        else:
            sender, msg = message.split(':', 1)
            print(f"\r\033[K<{sender}>:{msg}\n{name}: ", end="")
        sys.stdout.flush()


sHost = 'localhost'
sPort = 4000

cSocket = socket(AF_INET, SOCK_STREAM)
cSocket.connect((sHost, sPort))

name = input("Enter your name: ")
cSocket.send(name.encode())
print("[Press 'q' to exit]")

receive_thread = threading.Thread(target=receive_messages, args=(cSocket,))
receive_thread.start()

while True:
    message = input(f"{name}: ")
    if message == 'q':
        cSocket.send(f"q:quit".encode())
        break
    else:
        cSocket.send(f"{name}: {message}".encode())

cSocket.close()
