import socket
import threading
import os
import sys
import timeit
import time

global file_name
global BUFFER_SIZE
global SEPARATOR
BUFFER_SIZE = 16384
SEPARATOR = '<SEPARATOR>'

# TO-DO
# global host_socket
# clients list

host = socket.gethostbyname(socket.gethostname())
print(f'the host is : {host}')
port = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))

server_socket.listen(10)

def close_sockets(clients):
	for client in clients:
		print(f'[+]client {client} is closed')
		client.close()

def broadcast(data, clients):
	for client in clients:
		if client != host_socket:
			client.send(data)

def GUI_handler():
	while True:
		pass

def receive_from_host(le_code):

	clients = code [le_code] ['code_clients']
	host_socket = code [le_code] ['code_host']
	
	def unpad(s):
		return s[ : -ord(s[len(s) - 1 : ])]
	file_name = host_socket.recv(50).decode()

	print(f'[+]file name : {file_name}')
	broadcast(file_name.encode(), clients)

	start = timeit.default_timer()
	while True:
		clients = code [le_code] ['code_clients']
		data = host_socket.recv(BUFFER_SIZE)
		#print(f'received data : {data}')
		if 'end of file' in str(data):
			print(f'[+]eof received')
			print(f'[+]closing host-client sockets')
			#broadcast('EOF'.encode())
			broadcast(data, clients)
			host_socket.close()
			print('[+]host socket_closed')
			close_sockets(clients)
			clients.clear()
			break
		else:
			broadcast(data, clients)

		#if data == 'pre-EOF'.encode():
		#	print('inside the if statement')
		#	broadcast('pre-EOF'.encode())
		#	last_data = host_socket.recv(BUFFER_SIZE)
		#	broadcast(last_data)
		#	host_socket.close()
		#	break
		
	stop = timeit.default_timer()
	print(f'time taken to parse the file = {stop - start}')

if not os.path.exists(os.path.join(os.path.expanduser('~'), 'StreamIt')):
	os.mkdir(os.path.join(os.path.expanduser('~'), 'StreamIt'))
	
code = {}

#clients = []
while True:

	client_socket, address = server_socket.accept()

	with open(os.path.join(os.path.expanduser('~'), 'StreamIt', 'connection_logs.txt'), 'a') as le_file:
		le_file.write(f"{str(time.ctime())} \t {str(client_socket)} \n")

	print('[+]accepted a connection \n')
		
	# file_name, host_bool = client_socket.recv(2048).decode().split(SEPARATOR)
	# print(file_name)

	host_bool = client_socket.recv(11).decode()
	print(f'[+]host bool : {host_bool}')

	if host_bool == 'host':
		le_code = int(client_socket.recv(5).decode())
		if le_code not in list(code.keys()):
			client_socket.close()
		print('[+]host socket')
		print(f'[+]the code from host - {le_code} \n')
		global host_socket
		host_socket = client_socket
		code [le_code] ['code_host'] = host_socket
		recv_from_host_thread = threading._start_new_thread(receive_from_host, (le_code, ))

	elif host_bool == 'no host':
		le_code = int(client_socket.recv(5).decode())
		if le_code not in list(code.keys()):
			print('[+]invalid code received from connected client')
			client_socket.close()
			print('[+]client socket closed')
		print(f'[+]code received form client - {le_code}')
		code [le_code] ['code_clients'].append(client_socket)
		print('[+]client socket added to broadcast list \n')

	elif host_bool == 'GUI_socket':
		print('[+]GUI socket received')
		global GUI_socket
		GUI_socket = client_socket

	else:
		print('[+]code socket detected')
		le_code = client_socket.recv(1024).decode()
		le_code = int(le_code)
		if le_code in list(code.keys()):
			print('[+]pre-existing code received')
		else:
			code [le_code] = {'code_host' : '', 'code_clients' : []}

 	
	# broadcast(f"{file_name}{SEPARATOR}'host_bool'", host_socket)
