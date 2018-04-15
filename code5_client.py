#!/usr/bin/python3
# Import library socket
import socket
from threading import Thread
import sys

srv_ip, srv_port = sys.argv[1].split(":")
srv_sockaddr = (srv_ip, int(srv_port))

def handle_thread(conn):
    while True :
        try :
            data = conn.recv(100)
            data = data.decode('ascii')
            data, sender = data.split(" Sender ")
            print('\ndapat pesan dari {}'.format(sender))
            print('pesan\t: '+data)
        except(socket.error):
            # Tangkap error dari koneksi
            print("Koneksi ditutup")
            # Tutup koneksi
            conn.close()
            break

# Inisiasi object socket
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
confirm = 'N'

# Inisiasi 3-way handshaking/bikin koneksi
tcp_sock.connect(srv_sockaddr)
print('Client has been assigned socket name', tcp_sock.getsockname())
t=Thread(target=handle_thread, args=(tcp_sock,))
# Start thread baru
t.start()
print('================================================================')
while confirm == 'N':
    data = input()
    if data.upper() != 'CLOSE' : 
        print('Mengirim pesan "'+ data +'" ke server')
        tcp_sock.send( data.encode() )
    else:
        confirm = input('Apakah anda ingin mengakhiri Sesi? (Y/N)\t: ').upper()
print('================================================================')
# Tutup koneksi
tcp_sock.close()