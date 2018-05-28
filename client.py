import socket

host = '192.168.100.7'
port = 0

server = ('192.168.100.6', 4000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

message = input('Message to server: ')
while message != 'quit':
    message = message.encode('utf-8')
    sock.sendto(message, server)
    data, address = sock.recvfrom(1024)
    print('Server status: ' + str(data))
    message = input('Message to send: ')
sock.close()
