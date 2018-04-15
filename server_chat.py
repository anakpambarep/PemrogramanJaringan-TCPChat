#!/usr/bin/python3
# Program Server Chat
# author: erdiansahlan@student.ub.ac.id

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys

#menerima koneksi yang masuk
def accept_incoming_connections():
    while True: 
        client, client_address = SERVER.accept() 
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_address)).start()

#penanganan permintaan client
def handle_client(client,client_address):
    name = client.recv(BUFSIZ).decode("utf8")
    print('Client {} connected as {}'.format(client_address,name))
    welcome = "Welcome %s! type '/quit' to quit from the chat session" % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name 
    while True: 
        msg = client.recv(BUFSIZ)
        if msg != bytes("/quit", "utf8"):
            broadcast(msg, name)
        else:
            client.close()
            del clients[client]
            print('{} {} has disconnected'.format(name,client_address))
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

#broadcast pesan ke semua user kecuali pengirim pesan
def broadcast(msg, prefix=""):
    for sock in clients: 
        if clients[sock] != prefix: 
            sock.send(bytes(prefix+" : ", "utf8") + msg) 

clients = {}
addresses = {}

HOST,PORT=sys.argv[1].split(":")
BUFSIZ = 1024
ADDR = (HOST, int(PORT))

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__": 
    SERVER.listen(5)
    print("Server running..")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()