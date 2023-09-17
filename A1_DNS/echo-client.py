# echo-client.py

import socket
import subprocess

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1234  # The port used by the server

# subprocess.run(["python server.py"], shell=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while s:
        msg = input("Enter your message: ")
        if not msg:
            break
        s.sendall(msg.encode())
