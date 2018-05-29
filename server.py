import socket

host = socket.gethostname()
port = 4000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

print('Server is running as:', host)


def server():
    data, address = sock.recvfrom(1024)
    data = data.decode('utf-8')
    message = 'hi'
    message = message.encode('utf-8')
    sock.sendto(message, address)


while True:
    server()

sock.close()
