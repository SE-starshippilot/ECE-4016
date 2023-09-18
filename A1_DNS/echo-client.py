# echo-client.py

import socket
import subprocess

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1234  # The port used by the server

host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_socket.bind((HOST, PORT))
print(f"Server is listening on {HOST}:{PORT}")
while True:
    data, addr = host_socket.recvfrom(1024)
    print(f"Received from {addr}")
    print(data.decode('utf-8'))