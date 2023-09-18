import socket
import dnslib as dl
from dnslib.server import *

# Define the host and port to listen on
host = '127.0.0.1'
port = 1234

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((host, port))
    print(f"Server is listening on {host}:{port}")
    while True:
        msg, addr = server_socket.recvfrom(2048)
        query = dl.DNSRecord.parse(msg)
        
        server_socket.sendto(msg, addr)

