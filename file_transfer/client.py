import os
import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("localhost",9999))

file=open('/home/rishu/gitrepo/Socket/file_transfer/PathfinderCDS.pdf',"rb")   #opening file in byte read mode
file_size=os.path.getsize("/home/rishu/gitrepo/Socket/file_transfer/PathfinderCDS.pdf")    #return the size of file

client.send("received_file.pdf".encode())  #sending an encoded file received_image.jpg
client.send(str(file_size).encode())    #sending the size of the file

data=file.read()    #reading the content of the file
client.sendall(data)
client.send(b"<END>")   #to identify the end of file

file.close()
client.close()

