import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9292))
print('Waiting For Connection...')
server.listen(1)

client_connection, client_address = server.accept()
print('New Connection received!')

client_connection.close()
