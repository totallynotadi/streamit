import socket
import random
import os

code = int(''.join([str(random.randint(0, 9)) for i in range(5)]))
print(code)

#host = '192.168.43.164'
host = '18.116.67.97'
port = 5001

code_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

code_socket.connect((host, port))

code_socket.send('code socket'.encode())

code_socket.send(str(code).encode())

streamit_path = os.path.join(os.path.expanduser('~'), 'StreamIt', 'code.py')
print(streamit_path) 
with open('code.txt', 'w') as code_file:
	code_file.write(str(code))