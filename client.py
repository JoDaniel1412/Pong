import socket
from settings import *

host = socket.gethostname()
port = 0

server = ('Neptune', 4000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))


def client():
    message = 'HI'
    message = message.encode('utf-8')
    sock.sendto(message, server)
    data, address = sock.recvfrom(1024)
    data = data.decode('utf-8')


while True:
    client()

sock.close()
