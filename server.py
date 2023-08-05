import socket
import threading

HEADER = 64
PORT = 5000
FORMAT = "utf-8"
SERVER = socket.gethostbyname(socket.gethostname()) # Getting the IP address
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "[USER DISCONNECTED]"

# Creating a socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #AF_INET defines the IPv4 address,SOCK_STREAM streams the data through the server
server.bind(ADDR)   #Bind the system IP and Port to the new Socket

# Dictionary to store user information: username -(conn, addr)
user_data = {}

def handle_client(conn, addr):
    user = None

    # Receive the username from the client
    user_length = conn.recv(HEADER).decode(FORMAT)  #recv() waits until usernameis received and HEADER fixs the length of username
    if user_length:
        user_length = int(user_length)
        user = conn.recv(user_length).decode(FORMAT)
        user_data[user] = (conn, addr)
    print(f"[NEW CONNECTION] {addr} connected as {user}")
    for other_user, _ in user_data.items():
        if other_user != user:
            other_conn, _ = user_data[other_user]
            other_conn.send(f"[REQUEST]{user} wants to chat with you.".encode(FORMAT))
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)   #recv() waits until message is received and HEADER fixs the length of message
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:   # In case the user disconnect
                connected = False
            else:
                parts = msg.split(":", 1)   #Splits the message from :
                if len(parts) == 2:
                    receiver = parts[0]
                    message = parts[1]
                    if receiver in user_data:
                        receiver_conn, _ = user_data[receiver]
                        receiver_conn.send(f"[{user}] {message}".encode(FORMAT))    # Print whatever the message is
                    else:
                        print(f"USER[{receiver}] NOT FOUND!!")
                else:
                    print(f"INVALID MESSAGE FORMAT: {msg}")

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
