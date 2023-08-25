import socket
from struct import unpack
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 65000
server_address = (host, port)

sock.bind(server_address)
while True:
    # Wait for message
    message, address = sock.recvfrom(4096)

    s1, s2, s3 = unpack('3f', message)
    print(f's1: {s1}, s2: {s2}, s3: {s3}')
