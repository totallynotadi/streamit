from ffpyplayer.player import MediaPlayer
import threading
import cv2
import numpy
import os

def play_vid():
	audio_cap = MediaPlayer("C:\\vs code workspace1\\lol.mp4")
	video_cap = cv2.VideoCapture("C:\\vs code workspace1\\lol.mp4")

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
# play_vid()

def play_audio():
	pass

def write_file():
	with open(r'C:\vs code workspace1\stream\EP1.mp4', 'rb') as le_vid:
		with open('lol.mp4', 'wb') as lol_vid:
			while True:
				le_byte = le_vid.read(1024)
				lol_vid.write(le_byte)
				if len(le_byte) == 0:
					break 

write_thread = threading.Thread(group=None, target=write_file, name=None, args=(), kwargs=None, daemon=None)
write_thread.start()

play_thread = threading.Thread(group=None, target=play_vid, name=None, args=(), kwargs=None, daemon=None)
play_thread.start()
