# Jacob Miske
# GPL License
#!/usr/bin/python3

from operator import sub
import os, sys, random
import time
from matplotlib import image
import numpy as np
from numpy.core.fromnumeric import size
import matplotlib.pyplot as plt
import cv2
import cmd
from pyfiglet import Figlet
from src import Background as bg
from src import Frame as fr
from src import Message as ms
from src import Display as disp
from src import Instruction as ins

# Change on RPi before running
raspberry_pi = False

if raspberry_pi:
  import spidev
  spi1 = spidev.SpiDev()
  spi1.open(0,1)
  spi1.max_speed_hz = 250000
  spi1.bits_per_word = 8
  spi1.mode = 0
  spi2 = spidev.SpiDev(0, 1)
  spi2.max_speed_hz = 250000
else:
  print("WARNING")
  print("System is not setup to laser system")


class ScALP(cmd.Cmd):
  custom_fig = Figlet(font='slant')
  intro = 'Welcome to the ScALP CLI for Raspberry Pi \n'
  prompt = '> '
  file = None
  print(custom_fig.renderText(' ScALP '))


  def __init__(self):
    # Call on constructor of the parent class cmd.Cmd
    super(ScALP, self).__init__()
    self.ScALP_display = disp.Display()
    self.ScALP_instruction = ins.Instruction()


  def do_xy(self, arg):
    """
    Input instruction series object directly as an input i.e. [[0,0], [1,0], [1,1], [0,1]]
    Results in brief display of that instruction series
    """
    arg = []
    N = input("Number of points in instruction: ")
    for point in range(0, int(N)):
      print("Point {}".format(point))
      x = input("X coordinate: ")
      y = input("Y coordinate: ")
      arg.append([int(x), int(y)])
    xy_instruction = ins.Instruction()
    xy_instruction.instruct = arg
    if raspberry_pi:
          self.ScALP_display.display_single_instruction(instruct=xy_instruction.instruct, display_time=5)
    else:
      print("Not connected to display, plotting")
      self.ScALP_display.plot_single_instruction(instruct=xy_instruction.instruct)


  def do_xyRGB(self, arg):
    """
    Similar to do_xy but includes second argument list of color settings
    """
    arg = []
    color_list = []
    N = input("Number of points in instruction: ")
    for point in range(0, int(N)):
      print("Point {}".format(point))
      x = input("X coordinate: ")
      y = input("Y coordinate: ")
      # TODO: figure out the color input schema
      color = input("Color: (if no change, hit enter)")
      arg.append([int(x), int(y)])
      color_list.append(int(color))
    xy_instruction = ins.Instruction()
    xy_instruction.instruct = arg
    if raspberry_pi:
          self.ScALP_display.display_single_instruction(instruct=xy_instruction.instruct, display_time=5)
    else:
      print("Not connected to display, plotting")
      self.ScALP_display.plot_single_instruction(instruct=xy_instruction.instruct)


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
    while True:
      for count, point in enumerate(x, 0):
        x_val = int(x[count]) + 4096
        x_b_val = f'{x_val:016b}'
        hex1 = hex(int(x_b_val[0:8], 2))
        hex2 = hex(int(x_b_val[8:16], 2))
        hex1 = int(hex1, 16)
        hex2 = int(hex2, 16)
        spi1.writebytes([hex1, hex2])
        y_val = int(y[count]) + 36864
        y_b_val = f'{y_val:016b}'
        hex1 = hex(int(y_b_val[0:8], 2))
        hex2 = hex(int(y_b_val[8:16], 2))
        hex1 = int(hex1, 16)
        hex2 = int(hex2, 16)
        spi1.writebytes([hex1, hex2])

  def do_information(self, arg):
    """
    Get info on an image
    """
    frame = cv2.imread('./whitestar.jpg', cv2.IMREAD_GRAYSCALE)
    scale_percent = 30 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    contours = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(type(contours[1]))
    points = np.vstack(contours[1])
    # print(points)
    print(points[0])
    print("Number of Contours found = " + str(len(contours)))
    # cv2.drawContours(frame, contours[0], -1, (0, 255, 0), 3)
    # cv2.imshow('Contours', contours[0])
    # cv2.waitKey(0)
    # x = [float(i[0][0])*2 for i in points]
    # y = [float(i[0][1])*2 for i in points]
    x = list(range(0,1000,100)) + [1000]*10 + list(range(1000,0,-100)) + [0]*10
    y = [0]*10 + list(range(0,1000,100)) + [1000]*10 + list(range(1000,0,-100))
    print(x)
    print(y)
    cv2.destroyAllWindows()
    while True:
      for count, point in enumerate(x, 0):
        x_val = int(x[count]) + 4096
        x_b_val = f'{x_val:016b}'
        hex1 = hex(int(x_b_val[0:8], 2))
        hex2 = hex(int(x_b_val[8:16], 2))
        hex1 = int(hex1, 16)
        hex2 = int(hex2, 16)
        spi1.writebytes([hex1, hex2])
        y_val = int(y[count]) + 36864
        y_b_val = f'{y_val:016b}'
        hex1 = hex(int(y_b_val[0:8], 2))
        hex2 = hex(int(y_b_val[8:16], 2))
        hex1 = int(hex1, 16)
        hex2 = int(hex2, 16)
        spi1.writebytes([hex1, hex2])

  def do_image(self, arg):
    """
    reads image, creates point list
    """
    img = cv2.imread("./whitestar.jpg", cv2.IMREAD_UNCHANGED)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("example", img_grey)
    thresh = 100
    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = np.zeros(img.shape)
    contour_points = contours[1]
    #cv2.drawContours(img_contours, contours[1], -1, (0,255,0), 3)
    #cv2.imwrite("./contours.png", img_contours)
    # Now find equally spaced points along contours[1]
    xs = []
    ys = []
    print(contour_points)
    print(contour_points[0])
    for i in contour_points[0]:
      xs.append(i[0][0])
      ys.append(i[0][1])
    plt.figure(0)
    plt.scatter(ys, xs)
    plt.show()
    plt.close()
    # closed contour from xc to yc
    xc = xs + [xs[0]]
    yc = ys + [ys[0]]
    # find spacing between points
    dx = np.diff(xc)
    dy = np.diff(yc)
    dS = np.sqrt(dx*dx + dy*dy)
    print(dS)
    dS = [0] + list(dS)
    d = np.cumsum(dS)
    perimeter = d[-1]
    N = 50
    ds = perimeter/N
    dSi = [ds*i for i in range(0, N)]
    
    xi = np.interp(dSi, d, xc)
    yi = np.interp(dSi, d, yc)
    plt.figure(1)
    plt.scatter(yi, xi)
    plt.show()
    plt.close()
    x = [i*3 for i in xi]
    y = [j*3 for j in yi]
    while True:
      for count, point in enumerate(x, 0):
        x_val = int(x[count]) + 4096
        x_b_val = f'{x_val:016b}'
        hex1 = hex(int(x_b_val[0:8], 2))
        hex2 = hex(int(x_b_val[8:16], 2))
        hex1 = int(hex1, 16)
        hex2 = int(hex2, 16)
        spi1.writebytes([hex1, hex2])
        y_val = int(y[count]) + 36864
        y_b_val = f'{y_val:016b}'
        hex1 = hex(int(y_b_val[0:8], 2))
        hex2 = hex(int(y_b_val[8:16], 2))
        hex1 = int(hex1, 16)
        hex2 = int(hex2, 16)
        spi1.writebytes([hex1, hex2])
    pass

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
    scalp_ms.get_message()

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
  # draws a circle?
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
  c.cmdloop()
  sys.exit()
