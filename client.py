import socket
import threading

PORT = 10000     # Some unused port
SERVER = socket.gethostbyname(socket.gethostname()) # My local IP address
ADDR = (SERVER, PORT)
BUFFER_SIZE = 256
FORMAT = "utf-8"

def sending(sock):
    while True:
        my_msg = str(input("")).encode(FORMAT)
        sock.send(my_msg)

def receiving(sock):
    while True:
        recv_msg = sock.recv(BUFFER_SIZE).decode(FORMAT)
        print(recv_msg)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(ADDR)

t1 = threading.Thread(target=sending,args=(sock,))
t2 = threading.Thread(target=receiving,args=(sock,))

t1.start()
t2.start()