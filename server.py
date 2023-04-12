from socket import *
import threading

clients = {}


def client_handler(cSocket, address):
    client_name = cSocket.recv(1024).decode()
    clients[client_name] = cSocket
    print(f"[NEW CONNECTION] {client_name} connected from {address}.")

    message = f"{client_name} has joined the chat room."
    for name, socket in clients.items():
        if socket != cSocket:
            socket.send(message.encode())

    while True:
        data = cSocket.recv(1024)
        if not data:
            break

        message = data.decode()
        if message == 'q:quit':
            del clients[client_name]
            cSocket.close()
            print(f"[CONNECTION CLOSED] {client_name} disconnected.")
            message = f"{client_name} has left the chat room."
            for name, socket in clients.items():
                if socket != cSocket:
                    socket.send(message.encode())
            return

        sender, msg = message.split(':', 1)
        print(f"[{client_name}] {msg}")

        for name, socket in clients.items():
            if socket != cSocket:
                socket.send(message.encode())


sPort = 4000
sSocket = socket(AF_INET, SOCK_STREAM)
ADDR = ('localhost', sPort)
sSocket.bind(ADDR)

sSocket.listen(4)
print("The chat server is listening at ", ADDR)

while True:
    cSocket, address = sSocket.accept()
    print("Server connected with ", address)

    cThread = threading.Thread(target=client_handler, args=(cSocket, address))
    cThread.start()
