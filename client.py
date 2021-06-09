import socket
import time
import threading
import os
import shutil
import timeit

global app_dir
home_dir = os.path.expanduser('~')
app_dir = os.path.join(home_dir, 'StreamIt')
if not os.path.exists(app_dir):
	os.mkdir(app_dir)
	cache_path = os.path.join(app_dir, 'cache')
	os.mkdir(cache_path)
	saved_path = os.path.join(app_dir, 'saved')
	os.mkdir(saved_path)

host = '18.116.67.97'
#host = '192.168.43.164'
port = 5001

global BUFFER_SIZE
global SEPARATOR
BUFFER_SIZE = 16384
SEPARATOR = '<SEPARATOR>'

global client_socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))
print("[+]connected")

client_socket.send('no host'.encode())

code = str(input('enter the passcode for the stream : '))
client_socket.send(code.encode())
print('code sent')

def unpad(s):
		return s[ : -ord(s[len(s) - 1 : ])]
global file_name 
file_name = client_socket.recv(1024).decode()
file_name = unpad(file_name)
print(f'the file name is : {file_name}')

def receive_file():

	play_path = os.path.join(app_dir, 'cache', file_name)

	with open(play_path, 'wb') as receive_file:
		start = timeit.default_timer()
		while True:
			data = client_socket.recv(BUFFER_SIZE)
			#print(data)

			#if data == 'pre-EOF'.encode():
				#client_socket.recv(BUFFER_SIZE)
			if 'end of file' in str(data):
				print(data)
				print('EOF detected, so closing the socket')
				receive_file.write(data)
				client_socket.close()
				print('[+]client_socket_closed')
				break
			else:
				receive_file.write(data)
		stop = timeit.default_timer()

		print(f'time taken to receive the file = {stop - start}')

def play_video():

	video_path = os.path.join(app_dir, 'cache', file_name)

	print('playing the video lol \n')

	if os.name == 'nt':
		ffplay_path = os.getcwd() + '\\ffmpeg\\bin\\ffplay'
	else:
		ffplay_path = os.getcwd() + '//ffmpeg//bin//ffplay'
	os.system(f'{ffplay_path} {video_path}')

	'''
	if not os.path.exists('C:\\ffmpeg'):

		print("you don't have ffmpeg, so imma install that now")
		shutil.copytree(os.getcwd() + 'ffmpeg', 'C:\\ffmpeg')
		print('installed ffmpeg in your home directory! \n')
		print('playing the video now, enjoi!')
		os.system(r'set PATH = %PATH%; C:\ffmpeg\bin && ffplay ' + video_path)
	else:
		os.system(f'ffplay "{video_path}"')
	'''

receive_thread = threading.Thread(group=None, target=receive_file, name=None, args=(), kwargs=None, daemon=None)
receive_thread.start()

time.sleep(30)

#threading._start_new_thread(play_video, ())
play_thread = threading.Thread(group=None, target=play_video, name=None, args=(), kwargs=None, daemon=None)
play_thread.start()
