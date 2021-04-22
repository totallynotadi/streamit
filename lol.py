import cv2
import os

video_cap = cv2.VideoCapture("C:\\vs code workspace1\\stream\\EP1.mp4")

while video_cap.isOpened():
	ret, frame = video_cap.read()
	cv2.imshow('frame', frame)
	if cv2.waitKey(35) & 0xff == ord('q'):
		break

video_cap.release()
cv2.destroyAllWindows()
