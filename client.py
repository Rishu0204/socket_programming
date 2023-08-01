import socket

HEADER=64
PORT= 5000
FORMAT="utf-8"
DISCONNECT_MESSAGE = "[USER DISCONNECTED]"
SERVER="20.0.9.132"
ADDR=(SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message=msg.encode(FORMAT)  #encode the message from string to bit
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER -len(send_length))  #Adding padding to make the message 64 bit
    client.send(send_length)
    client.send(message)
    print(client.recv(5000).decode(FORMAT))
    

# send("HELLO")
while True:
    say=input("ENTER YOUR MESSAGE: ")
    send(say)
    disconnect="bye"
    if say==disconnect:
        send(DISCONNECT_MESSAGE)
        break

