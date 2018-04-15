#!/usr/bin/python3
# Program Client Chat
# author: erdiansahlan@student.ub.ac.id

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys 

#menerima pesan/broadcast dari server
def receive():
    while True:
        try: 
            msg = client_socket.recv(BUFSIZ).decode("utf8") 
            print(msg) 
        except OSError:
            break

#mengirim pesan ke server untuk di broadcast 
def send(msg):  # event is passed by binders. 
    client_socket.send(bytes(msg, "utf8")) 
    if msg == "/quit": 
         client_socket.close() 

HOST, PORT=sys.argv[1].split(":")
NAME = sys.argv[2]

BUFSIZ = 1024
ADDR = (HOST, int(PORT)) 

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR) 
client_socket.send(bytes(NAME, "utf8")) 
receive_thread = Thread(target=receive) 
receive_thread.start() 

while True: 
    msg = input() 
    send(msg) 
    if msg=="/quit": 
         print("Goodbye..")
         break