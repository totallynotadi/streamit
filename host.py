from tkinter import filedialog
import tkinter
import socket
import time 
import threading
import os
import shutil
import timeit

# TO-DO
# try a complete run with no ffmpeg in c drive

host = '18.116.67.97'
#host = '192.168.43.164'
port = 5001

global BUFFER_SIZE
global SEPARATOR
BUFFER_SIZE = 16384
SEPARATOR = '<SEPARATOR>'

global host_socket
host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_socket.connect((host, port))

host_socket.send('host'.encode())
time.sleep(1)

global file_name

root = tkinter.Tk()
root.withdraw()

global file_path
file_path = filedialog.askopenfilenames() [0]

base_path, file_name = os.path.split(file_path)

code = str(input('enter the passcode for the stream : '))
host_socket.send(code.encode())
	
def pad(s, n):
	return s + (n - len(s) % n) * chr(n - len(s) % n)
file_name = pad(file_name, 50)
host_socket.send(file_name.encode())

# host_socket.send('host_lol'.encode())

def send_file():

	with open(file_path, 'rb') as the_file:
		file_size = os.stat(file_path).st_size
		print(file_size)	
		start = timeit.default_timer()
		while True:
			data = the_file.read(BUFFER_SIZE)

			if not data:
				print(the_file.tell())
				print(len(data))
				print(data)
				host_socket.send('end of file'.encode())
				host_socket.close()
				print('sent EOF')
				print('the file is over')
				break
			else:
				host_socket.send(data)

			#if the_file.tell() >= file_size - 8192:
				#break

		#host_socket.send('pre-EOF'.encode())
		#time.sleep(0.5)
		#host_socket.send(the_file.read(BUFFER_SIZE))
		#host_socket.close()

			# print(f'sent data : {data}')
		stop = timeit.default_timer()
		total_time = stop - start
		print('file sent lol')
		print(f'time taken to send the file = {total_time}')

def play_video():
	time.sleep(3)

	'''   deprecated way, audio sucks on some videos lol
	audio_cap = MediaPlayer(file_name)
	video_cap = cv2.VideoCapture(file_name)	

	while video_cap.isOpened():
		ret, frame = video_cap.read()
		audio_frame, val = audio_cap.get_frame()

		cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
		cv2.setWindowProperty('frame', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)

		FPS = int(numpy.round((1/video_cap.get(cv2.CAP_PROP_FPS) * 1000)))

		if cv2.waitKey(35) & 0xff == ord('q'): #35 also works for waitkey 
			break

		cv2.imshow('frame', frame)
		if val != 'eof' and audio_frame != None:
			img, t = audio_frame

	video_cap.release()
	cv2.destroyAllWindows()
	'''

	def flip_slash(s):
		return s.replace('/', '\\')

	ffplay_path = os.getcwd() + '\\ffmpeg\\bin\\ffplay'
	#print(ffplay_path)
	#os.system(f'{ffplay_path} {file_path} -hide_banner')
	#file_path = file_path.replace('/', '\\')
	print(file_path )

	if os.name == 'nt':
		os.system(f"vlc {flip_slash(file_path)}")
	else:
		os.system(f"{ffplay_path} {file_path}")

	'''
	if os.path.exists('C:\\ffmpeg') == False:
		print(os.path.exists('C:\\ffmpeg'))
		print(file_path)
		print(os.getcwd())
		print(os.path.join(os.getcwd(), '\\ffmpeg'))
		shutil.copytree(os.getcwd() + '\\ffmpeg', 'C:\\ffmpeg')
		
		os.system(r'set PATH = %PATH%; C:\ffmpeg\bin && ffplay ' + file_path)
		print(file_path)
		print('in the if block')
	else:
		print('in the else block')
		os.system(f'ffplay "{file_path}"')
	'''

send_thread = threading.Thread(group=None, target=send_file, name=None, args=(), kwargs=None, daemon=None)
send_thread.start()

play_thread = threading.Thread(group=None, target=play_video, name=None, args=(), kwargs=None, daemon=None)
play_thread.start()
