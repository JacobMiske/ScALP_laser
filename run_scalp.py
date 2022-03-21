# Jacob Miske
# GPL License
#!/usr/bin/python3

from operator import sub
import os, sys, random
import time
from matplotlib import image
import numpy as np
from numpy.core.fromnumeric import size
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import cv2
import cmd
from pyfiglet import Figlet
from src import Background as bg
from src import Frame as fr
from src import Message as ms

raspberry_pi = True

if raspberry_pi:
  import spidev
  spi1 = spidev.SpiDev()
  spi1.open(0,1)
  spi1.max_speed_hz = 250000
  spi1.bits_per_word = 8
  spi1.mode = 0
  spi2 = spidev.SpiDev(0, 1)
  spi2.max_speed_hz = 250000


class ScALP(cmd.Cmd):
  custom_fig = Figlet(font='slant')
  intro = 'Welcome to the ScALP CLI for Raspberry Pi \n'
  prompt = '> '
  file = None
  print(custom_fig.renderText(' ScALP '))
  

  def do_background(self, arg):
    scalp_bg = bg.Background()
    scalp_bg.set_background()
	

  def do_frame(self, arg):
    scalp_fr = fr.Frame()
    scalp_fr.set_frame()


  def do_xy(self, arg):
    """
    For each frame in background and foreground, subtract, Canny edge detection, find contours, get x-y
    """
    back = cv2.VideoCapture('./background_video.avi')
    fore = cv2.VideoCapture('./foreground_video.avi')
    back_frames = []
    fore_frames = []
    diff_frames = []
    for i in range(60):
      _, back_frame = back.read()
      _, fore_frame = fore.read()
      back_gray = cv2.cvtColor(back_frame, cv2.COLOR_BGR2GRAY)
      fore_gray = cv2.cvtColor(fore_frame, cv2.COLOR_BGR2GRAY)
      back_frames.append(back_gray)
      fore_frames.append(fore_gray)
    threshold = 40
    for i in range(0, 5):
      print("frame: " + str(i))
      f_frame = fore_frames[i]
      b_frame = back_frames[i]
      diff_frame = np.zeros(shape=(720, 1280))
      for x in range(0, 720):
        for y in range(0, 1280):
          pixel = int(f_frame[x, y]) - int(b_frame[x,y])
          if abs(pixel) > threshold:
            diff_frame[x, y] = 1
      diff_frames.append(diff_frame)
    avg_img = np.mean(diff_frames, axis=0)
    labeled_image, nb_labels = ndimage.label(diff_frames[-1], structure=np.ones((3,3)))
    sizes = ndimage.sum(diff_frames[-1], labeled_image, range(nb_labels + 1))
    sizes = list(sizes)
    main_label = max(sizes)
    res_list = [i for i, value in enumerate(sizes) if value == main_label]
    main_label = res_list[0]
    for x in range(0, 720):
      for y in range(0, 1280):
        if labeled_image[x, y] != main_label:
          labeled_image[x, y] = 0
        else:
          labeled_image[x, y] = 255
    cv2.imwrite('./labels.jpg', labeled_image)
    image_bw = ndimage.binary_fill_holes(labeled_image).astype(int)
    cv2.imwrite('./label_bw_filled_in.jpg', image_bw)

    # while True:
    #   cv2.imshow('Gray image', diff_frames[-1])
    #   k = cv2.waitKey(33)
    #   if k==27:    # Esc key to stop
    #       break
    cv2.destroyAllWindows()


  def do_xyRGB(self, arg):
    """
    Similar to do_xy but looks at whole RGB
    """
    back = cv2.VideoCapture('./background_video.avi')
    fore = cv2.VideoCapture('./foreground_video.avi')
    back_frames = []
    fore_frames = []
    diff_frames = []
    for i in range(60):
      _, back_frame = back.read()
      _, fore_frame = fore.read()
      back_frames.append(back_frame)
      fore_frames.append(fore_frame)
    threshold = 110
    for i in range(0, 5):
      print("frame: " + str(i))
      f_frame = fore_frames[i]
      b_frame = back_frames[i]
      diff_frame = np.zeros(shape=(720, 1280))
      for x in range(0, 720):
        for y in range(0, 1280):
          red_pixel = abs(int(f_frame[x, y][0]) - int(b_frame[x,y][0]))
          green_pixel = abs(int(f_frame[x, y][1]) - int(b_frame[x,y][1]))
          blue_pixel = abs(int(f_frame[x, y][2]) - int(b_frame[x,y][2]))
          pixel_diff = red_pixel + green_pixel + blue_pixel
          if abs(pixel_diff) > threshold:
            diff_frame[x, y] = 255
      diff_frames.append(diff_frame)
    cv2.imwrite('./diff_frame.jpg', diff_frames[0])
    labeled_image, nb_labels = ndimage.label(diff_frames[-1], structure=np.ones((3,3)))
    sizes = ndimage.sum(diff_frames[-1], labeled_image, range(nb_labels + 1))
    sizes = list(sizes)
    main_label = max(sizes)
    res_list = [i for i, value in enumerate(sizes) if value == main_label]
    main_label = res_list[0]
    for x in range(0, 720):
      for y in range(0, 1280):
        if labeled_image[x, y] != main_label:
          labeled_image[x, y] = 0
        else:
          labeled_image[x, y] = 255
    cv2.imwrite('./labels_RGB.jpg', labeled_image)
    image_bw = ndimage.binary_fill_holes(labeled_image).astype(int)
    cv2.imwrite('./label_bw_filled_in_RGB.jpg', image_bw)
    cv2.destroyAllWindows()


  def do_drivexy(self, arg):
    """
    Drives the digital signal to send the laser to
    a specific point. Can be called <=800 times a second.
    Uses a list of x and y points.
    """
    for i in range(100, 4000, 100):
      val = int(i) + 4096
      binary_val = f"{val:016b}"
      hex1 = hex(int(binary_val[0:8], 2))
      hex2 = hex(int(binary_val[8:16], 2))
      hex1 = int(hex1, 16)
      hex2 = int(hex2, 16)
      spi1.writebytes([hex1, hex2])
      spi2.writebytes([hex1, hex2])
      time.sleep(0.005)
    for i in range(4000, 100, -100):
      val = int(i) + 4096
      binary_val = f'{val:016b}'
      hex1 = hex(int(binary_val[0:8], 2))
      hex2 = hex(int(binary_val[8:16], 2))
      hex1 = int(hex1, 16)
      hex2 = int(hex2, 16)
      spi1.writebytes([hex1, hex2])
      spi2.writebytes([hex1, hex2])
      time.sleep(0.005)
    

  def do_circle(self, arg):
    """
    Drives motor to make a circle
    """
    points = 100
    angles = np.linspace(0, 2*3.14159, points)
    input_x = input("Provide center x (int): ")
    input_y = input("Provide center y (int): ")
    x = float(input_x)
    y = float(input_y)
    input_radius = input("Provide radius (int less than 1000): ")
    angles = [float(i) for i in list(angles)]
    input_radius = float(input_radius)
    x = [round(input_radius * np.cos(angle)) + x for angle in angles]
    y = [round(input_radius * np.sin(angle)) + y for angle in angles]
    for count, point in enumerate(x, 0):
      x_val = int(x[count]) + 4096
      x_b_val = f'{x_val:016b}'
      hex1 = hex(int(x_b_val[0:8], 2))
      hex2 = hex(int(x_b_val[8:16], 2))
      hex1 = int(hex1, 16)
      hex2 = int(hex2, 16)
      spi1.writebytes([hex1, hex2])
      y_val = int(y[count]) + 65536
      y_b_val = f'{y_val:016b}'
      hex1 = hex(int(y_b_val[0:8], 2))
      hex2 = hex(int(y_b_val[8:16], 2))
      hex1 = int(hex1, 16)
      hex2 = int(hex2, 16)
      spi1.writebytes([hex1, hex2])
      time.sleep(0.005)
    

  def do_information(self, arg):
    """
    Get info on an image
    """
    frame = cv2.imread('./background_frame.jpg')
    print(frame[0,0])
    cv2.destroyAllWindows()

  def do_colorpick(self, arg):
    """
    Drives the digital signal to achieve the correct
    RGB color on the white laser
    """
    pass

  def do_threshold(self, arg):
    """
    Test thresholding to determine outline points
    """
    
    pass

  def do_message(self, arg):
    scalp_ms = ms.Message()

  def do_bye(self, arg):
    """
    Stop command line interface
    """
    print('thanks for using scalp')
    self.close()
    return True

  def close(self):
    if self.file:
        self.file.close()
        self.file = None


def bitstring_to_bytes(s):
  v = int(s, 2)
  b = bytearray()
  while v:
    b.append(v & 0xFF)
    v >>= 8
    return bytes(b[::-1])


def set_int_to_DAC():
  for i in range(100, 4000, 100):
    val = int(i) + 4096
    binary_val = f'{val:016b}'
    res = bitstring_to_bytes(binary_val)
    hex1 = hex(int(binary_val[0:8], 2))
    hex2 = hex(int(binary_val[8:16], 2))
    hex1 = int(hex1, 16)
    hex2 = int(hex2, 16)
    spi1.writebytes([hex1, hex2])
    spi2.writebytes([hex1, hex2])
    time.sleep(0.005)
  for i in range(4000, 100, -100):
    val = int(i) + 4096
    binary_val = f'{val:016b}'
    res = bitstring_to_bytes(binary_val)
    hex1 = hex(int(binary_val[0:8], 2))
    hex2 = hex(int(binary_val[8:16], 2))
    hex1 = int(hex1, 16)
    hex2 = int(hex2, 16)
    spi1.writebytes([hex1, hex2])
    spi2.writebytes([hex1, hex2])
    time.sleep(0.005)


if __name__ == '__main__':
  c = ScALP()
  sys.exit(c.cmdloop())
