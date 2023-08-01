import socket 
import threading

HEADER=64
PORT= 5000
FORMAT="utf-8"
SERVER=socket.gethostbyname(socket.gethostname())  #GETS HOST IP FROM THE SYSTEM
ADDR=(SERVER,PORT)
DISCONNECT_MESSAGE = "[USER DISCONNECTED]"

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #AF_INET defines the IPv4 address,SOCK_STREAM streams the data through the server
server.bind(ADDR)  #Bind the system IP and Port to the new Socket

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)    #recv() waits until message is recived and HEADER fixs the length of message
        # decode() convert the byte message into string using utf-8
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:   # In case the user disconnect
                connected = False
            print(f"[{addr}] {msg}")    # Print whatever the message is

            conn.send("[MESSAGE RECEIVED]".encode(FORMAT))
    conn.close()    # Closes the connection

def start():
    server.listen() #Puts the server into listen mode i.e. waiting for the connection to happen
    print(f"[SERVER LISTENING] on {SERVER}")
    while True:
        conn, addr = server.accept()    #Accepts the new connections
        thread = threading.Thread(target=handle_client,args=(conn,addr))  #Creating new thread for each connection for parallel communication
        thread.start()  #Starts the thread
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")  #threading.activeCount() gives the total number of threads in use


print("[STARTING] server is starting.....")
start()
