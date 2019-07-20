# GPL License
#!/usr/bin/python3

import os, sys
import numpy as np
import cv2
import time
import pygame
import cmd
from pyfiglet import Figlet

class ScALP(cmd.Cmd):
  custom_fig = Figlet(font='slant')
  intro = 'Welcome to the ScALP CLI for Raspberry Pi \n'
  prompt = '> '
  file = None
  print(custom_fig.renderText(' ScALP '))
  
  def do_webcam(self, arg):
    '''
    Initialize the webcam, take a test frame for 5 seconds
    '''
    cam = cv2.VideoCapture(0)
    
    ret, image = cam.read()
    if ret:
      # Create window to show image
      cv2.imshow('test', image)
      # Show window for 5 seconds
      cv2.waitKey(5000)
      cv2.destroyWindow('test')
      # Write image to Desktop
      cv2.imwrite('/home/pi/Desktop/ScALP/ScALP_laser/test.jpg', image)
    cam.release()
    pass
	
  def do_frame(self, arg):
    '''
    Takes a frame from the webcam
    '''
    cam = cv2.VideoCapture(0)
    # Open USB webcam in cv2 and take a picture then release camera
    cam.open(0)
    retval, image = cam.retrieve()
    cam.release()
    cv2.imwrite('/home/pi/Desktop/ScALP/ScALP_laser/test.jpg', image)
    img = cv2.imread('/home/pi/Desktop/ScALP/ScALP_laser/test.jpg', 0)

    ## cv2.imshow('image', img)
    ## cv2.waitKeys(0)
    ## cv2.destroyAllWindows()
    
    # Run edge detection, edges is a numpy.ndarray
    edges = cv2.Canny(img, 100, 200)
    print(type(edges))
    print(edges)
    edge_nz = np.nonzero(edges)
    print('Indices of non-zero elements: ', edge_nz)
    time.sleep(1)

	
  def do_x_y(self, arg):
    '''
    From a frame, creates lists of x and y point of images
    '''
    pass
    

  def do_x_y(self, arg):
    '''
    Drives the digital signal to send the laser to
    a specific point. Can be called <=800 times a second
    '''
    pass


  def do_colorpick(self, arg, r,g,b):
    '''
    Drives the digital signal to achieve the correct
    RGB color on the white laser
    '''
    pass

  def do_bye(self, arg):
    '''
    Stop cmd
    '''
    print('thanks for using scalp')
    self.close()
    return True

  def close(self):
    if self.file:
        self.file.close()
        self.file = None


if __name__ == '__main__':
        c = ScALP()
        sys.exit(c.cmdloop())
