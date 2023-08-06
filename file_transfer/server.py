import socket
import tqdm

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost",9999))
server.listen() #server in listen mode

client,addr=server.accept() #accepting client

file_name=client.recv(1024).decode()  #receiveing file name recevied_image.jpg
print(file_name)
file_size=client.recv(1024).decode()    #receiving file size
print(file_size)

file=open(file_name,"wb")   #opening file in write byte mode
file_bytes=b""     #initializing empty string to append bytes

done=False
#progress bar
progress=tqdm.tqdm(unit="B",unit_scale=True,unit_divisor=1000,total=int(file_size))

while not done:
    data =client.recv(1024)
    if file_bytes[-5:]==b"<END>":   #checking last 5 character, if its <END> then complete file is transfered
        done=True
    else:
        file_bytes+=data    #keep appending the file_bytes
    progress.update(1024)   #updating progress bar

file.write(file_bytes)  #writing all the content of the file received file in "recevied_image.jpg"
file.close()
client.close()
server.close()
