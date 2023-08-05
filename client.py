import socket
import threading
HEADER = 64
PORT = 5000
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "[USER DISCONNECTED]"
SERVER = "20.0.10.136"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket for the client
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)    #encode the message from string to bit
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))   #Adding padding to make the message 64 bit
    client.send(send_length)
    client.send(message)
    print(client.recv(5000).decode(FORMAT))

def send_username(user):
    message = user.encode(FORMAT)   #encode the message from string to bit
    user_length = len(message)
    send_length = str(user_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))   #Adding padding to make the message 64 bit
    client.send(send_length)
    client.send(message)

def send_disconnect():
    send(DISCONNECT_MESSAGE)
    client.close()

user = input("ENTER YOUR USERNAME: ")
send_username(user)

# receiver = input("WHO DO YOU WANT TO CHAT WITH: ")
# # print(f"Connected with {receiver}")
# send(f"{receiver}:[REQUEST]{user} WANTS TO CHAT WITH YOU")
# choice = input("Do you want to send messages? (yes/no): ")
# def sendMessageLoop():
#     while True:
    
#         # request_message = f"[REQUEST]{user} WANTS TO CHAT WITH YOU"
#         # send(f"{receiver}:{request_message}")  # Sending a request message
        
#         say = input("ENTER YOUR MESSAGE: ")
#         send(f"{receiver}:{say}")
       
#         if say.lower() == "bye":
#             send_disconnect()
#             break
# if choice.lower()=="yes":
#     while True:
    
#         # request_message = f"[REQUEST]{user} WANTS TO CHAT WITH YOU"
#         # send(f"{receiver}:{request_message}")  # Sending a request message
        
#         say = input("ENTER YOUR MESSAGE: ")
#         send(f"{receiver}:{say}")
       
#         if say.lower() == "bye":
#             send_disconnect()
#             break
#         send(f"{receiver}:{user} says: {say}")
#     send_disconnect()

        
# #     message_thread = threading.Thread(target=sendMessageLoop)  #Start the message loop in a separate thread
# #     message_thread.start()
# #     message_thread.join()   #it waits for the message loop thread to complete before proceeding to close the client connection

# # else:
    
# #     print("Waiting for the other user to start the conversation...")    # Wait for the recipient to initiate the conversation
# #     response = client.recv(5000).decode(FORMAT)
# #     print(response) # Print the message from the other user
# # send_disconnect()
# client.close()
role_choice = input("Do you want to act as the sender or receiver? (sender/receiver): ")
if role_choice.lower() == "sender":
    receiver = input("WHO DO YOU WANT TO SEND TO: ")
    message = input("ENTER YOUR MESSAGE: ")
    send(f"{receiver}:{message}")
else:
    print("Waiting for incoming messages...")

while True:
    msg = client.recv(5000).decode(FORMAT)
    print(msg)
    if msg.startswith("[sender]"):
        reply = input("Enter your reply/message: ")
        send(f"{msg[8:]}:{reply}")

    if msg == DISCONNECT_MESSAGE:
        print("Disconnected.")
        break

send_disconnect()