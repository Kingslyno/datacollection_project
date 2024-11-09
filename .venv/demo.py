import socket

SKT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SKT.bind((socket.gethostname(), 6060))
SKT.listen(5)

while True:
    Client_Socket, Adress = SKT.accept()
    print(f"Connection has been established from {Adress}")
    Client_Socket.send(bytes("Welcome to the server!!!", "utf-8"))
    Client_Socket.close()