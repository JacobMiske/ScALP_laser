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
    Initialize the webcam, take a test frame
    '''
    cam = cv2.VideoCapture(0)
    
    ret, image = cam.read()
    if ret:
      cv2.imshow('test', image)
      cv2.waitKey(5000)
      cv2.destroyWindow('test')
      cv2.imwrite('/home/pi/test.jpg', image)
    cam.release()
    pass
	
  def do_frame(self, arg):
    '''
    Takes a frame from the webcam
    '''
    pass

	
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
