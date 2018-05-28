import socket

host = '192.168.100.7'
port = 4000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

print('Server Running')
message = 'Server is running'
while message != 'quit':
    data, address = sock.recvfrom(1024)
    print('From: ' + str(address) + ': :' + str(data))
    message = input('Message to client: ')
    print('sending... ' + ': :' + message)
    message = message.encode('utf-8')
    sock.sendto(message, address)
sock.close()
