import socket
import threading

PORT = 10000     # Some unused port
SERVER = socket.gethostbyname(socket.gethostname()) # My local IP address
ADDR = (SERVER, PORT)
BUFFER_SIZE = 256
FORMAT = "utf-8"

mydict = {} # DICTIONARY: keys are topics and values are lists of subscribers

def subscribe(msg,conn):
    if msg not in mydict:
        mylist = []
        mylist.append(conn)
        mydict[msg] = mylist
    else: 
        mydict[msg].append(conn)

    conn.send(("[SUCCESS]").encode(FORMAT))


def publish(topic,msg,conn):
    if topic in mydict:
        for subscriber in mydict[topic]:
            subscriber.send((topic + ": " + msg).encode(FORMAT))

    conn.send(("[SUCCESS]").encode(FORMAT))

def handle_connection(conn, addr):
    conn.send(("SUB sometopicname - to subscribe to a topic \nPUB sometopicname message - to send a message to a topic").encode(FORMAT))

    while True:
        msg = str(conn.recv(BUFFER_SIZE).decode(FORMAT))
        # RECEIVED A MESSAGE
        # PARSING MESSAGE
        if msg.startswith('SUB '):
            msg = msg[len('SUB '):].upper()
            subscribe(msg,conn)
        elif msg.startswith('PUB '):
            is_valid = True
            msg = msg[len('PUB '):]
            index = msg.find(" ")
            if index <= 0:
                is_valid = False
            topic = msg[:index].upper()
            msg = msg[index+1:]
            if len(msg) <= 0:
                is_valid = False
            
            if is_valid:
                publish(topic,msg,conn)
            else:
                conn.send(("Invalid query - missing topic name or message ").encode(FORMAT))
        else: 
            # Useless message...
            conn.send(("Invalid query - need to have SUB or PUB in front of message... ").encode(FORMAT))


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(ADDR) # If a client connects to ADDR it will reach socket

    # Starting server 
    print("Starting server")
    sock.listen()

    while True:

        # Accepting incoming connections
        conn, addr = sock.accept()  
        print("Accepted connection from " + str(addr))  

        # Forming a thread to handle new connection
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        t.start()

        print("Active connections: " + str(threading.active_count() - 1))


if __name__ == "__main__":
    run()
    

        