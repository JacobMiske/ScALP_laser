# GPL License

import numpy as np
import cv2
import time


def start_webcam():
	'''
	Initialized the webcam
	'''
	vidcap = cv2.VideoCapture(0)
	vidcap.open(0)
	retval, image = vidcap.retrieve()
	time.sleep(0.5)
	vidcap.release()
	cv2.imwrite("test.png", image)

	
def take_frame():
	'''
	Takes a frame from the webcam
	'''
	pass

	
def create_x_y():
	'''
	From a frame, creates lists of x and y point of images
	'''
	pass
	

def send_x_y():
	'''
	Drives the digital signal to send the laser to 
	a specific point. Can be called <=800 times a second
	'''
	pass


def color_selection(r,g,b):
	'''
	Drives the digital signal to achieve the correct
	RGB color on the white laser
	'''
	pass

start_webcam()
