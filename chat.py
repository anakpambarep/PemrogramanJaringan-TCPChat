#!/usr/bin/python3
# Program Chat Server
# author: mahendra.data@ub.ac.id
# execute: ./chatserver.py <"server"/"client"> <IP>:<PORT>

import select
import signal
import socket
import sys

#class untuk server
class Server:
    def __init__(self, sockaddr):
        self.connsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connsock.bind(sockaddr)
        self.socklist = [self.connsock]

    def __serve__(self, readysock):
        for sock in readysock:
            datasock, clientsockaddr = self.connsock.accept()
            datasock.setblocking(0)
            self.socklist.insert(0, datasock)
            print('Client {} connected'.format(clientsockaddr))
        else:
            self.__broadcast__(sock)

    def __broadcast__(self, sock):
        data = sock.recv(2048)
        data = "{} > ".format(sock.getpeername()).encode("utf-8") + data
        if data:
            for s in self.socklist[:-1]:
                if s.getpeername() != sock.getpeername():
                    s.sendall(data)
        else:
            self.socklist.remove(sock)
            print('Client {} disconnected'.format(sock.getpeername()))
            sock.close()

    def run(self):
        self.connsock.listen(1)
        print("Listening at ", self.connsock.getsockname())
        print("Press Ctrl+c to exit...")
        while True:
            try:
                signal.signal(signal.SIGINT, signal.default_int_handler())
                readysock, _, _ = select.select(self.socklist, [], [])
                self.__serve__(readysock)
            except KeyboardInterrupt:
                break
        for s in self.socklist:
            s.close()

#class untuk client
class Client:
    def __init__(self, sockaddr):
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsock.connect(sockaddr)
        self.inputlist = [sys.stdin, self.clientsock]
        self.online = True

    def __serve__(self, readyinput):
        for ri in readyinput:
            if ri is self.clientsock:
                data = self.clientsock.recv(2048)
                if data:
                    print(data.decode("utf-8"))
                else:
                    print('Server {} disconnected'.format(self.clientsock.getpeername()))
                    self.online = False
                    break
            else:
                data = sys.stdin.readline().strip()
                self.clientsock.sendall(data.encode("utf-8"))

    def run(self):
        print("Press Ctrl+c to exit...")
        while self.online:
            try:
                signal.signal(signal.SIGINT, signal.default_int_handler())
                readyinput, _, _ = select.select(self.inputlist, [], [])
                self.__serve__(readyinput)
            except KeyboardInterrupt:
                break
        self.clientsock.close()

if __name__ == '__main__':
    ip, port = sys.argv[2].split(":")
    sockaddr = (ip, int(port))
    apps = Server(sockaddr) if sys.argv[1] == "server" else Client(sockaddr)
    apps.run()