# Jacob Miske
# This is a CLI to interact with the ScALP System
# GPL License
#!/usr/bin/python3

# Import libraries and modules
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
  print("System is not setup to laser system, software will plot locally instead of drive laser")


class ScALP(cmd.Cmd):
  custom_fig = Figlet(font='slant')
  intro = 'Welcome to the ScALP CLI \n'
  prompt = '> '
  file = None
  print(custom_fig.renderText(' ScALP '))


  def __init__(self):
    # Call on constructor of the parent class cmd.Cmd
    super(ScALP, self).__init__()
    self.ScALP_display = disp.Display()
    self.ScALP_instruction = ins.Instruction()
    self.ScALP_frame = fr.Frame()


  def do_xy(self, arg):
    """
    Input instruction series object directly as an input i.e. [[0,0], [1,0], [1,1], [0,1]]
    Results in brief display of that instruction series
    """
    points = []
    N = input("Number of points in instruction: ")
    for point in range(0, int(N)):
      print("Point {}".format(point))
      x = input("X coordinate: ")
      y = input("Y coordinate: ")
      points.append([int(x), int(y)])
    xy_instruction = ins.Instruction()
    xy_instruction.instruct = points
    if raspberry_pi:
      # display for 5 seconds
      self.ScALP_display.display_single_instruction(instruct=xy_instruction.instruct, display_time=5)
    else:
      print("Not connected to display, plotting")
      self.ScALP_display.plot_single_instruction(instruct=xy_instruction.instruct)


  def do_xyRGB(self, arg):
    """
    Similar to do_xy but includes second argument list of color settings
    """
    points = []
    color_list = []
    N = input("Number of points in instruction: ")
    for point in range(0, int(N)):
      print("Point {}".format(point))
      x = input("X coordinate: ")
      y = input("Y coordinate: ")
      # TODO: figure out the color input schema
      color = input("Color: (if no change, hit enter)")
      points.append([int(x), int(y)])
      color_list.append(int(color))
    xy_instruction = ins.Instruction()
    xy_instruction.instruct = points
    if raspberry_pi:
          self.ScALP_display.display_single_instruction(instruct=xy_instruction.instruct, display_time=5)
    else:
      print("Not connected to display, plotting")
      self.ScALP_display.plot_single_instruction(instruct=xy_instruction.instruct)
    

  def do_circle(self, arg):
    """
    Drives system to make a circle
    """
    points = []
    points_in_circle = 100
    angles = np.linspace(0, 2*3.14159, points_in_circle)
    input_x = input("Provide center x (int): ")
    input_y = input("Provide center y (int): ")
    x = float(input_x)
    y = float(input_y)
    input_radius = input("Provide radius (int less than 1000): ")
    angles = [float(i) for i in list(angles)]
    input_radius = float(input_radius)
    x = [round(input_radius * np.cos(angle)) + x for angle in angles]
    y = [round(input_radius * np.sin(angle)) + y for angle in angles]
    circle_instruction = ins.Instruction()
    # Generate list of lists as instruction.instruct object
    for i in range(0, len(x)):
      points.append([x[i], y[i]])
    circle_instruction.instruct = points
    # Two options based on system
    if raspberry_pi:
      self.ScALP_display.display_single_instruction(instruct=circle_instruction.instruct, display_time=5)
    else:
      print("Not connected to display, plotting")
      self.ScALP_display.plot_single_instruction(instruct=circle_instruction.instruct)


  def do_information(self, arg):
    """
    Get information on a saved image
    """
    frame = cv2.imread('./media/whitestar.jpg', cv2.IMREAD_GRAYSCALE)
    scale_percent = 30 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    contours = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(type(contours[1]))
    image_points = np.vstack(contours[1])
    # print(points)
    print(image_points[0]) 
    print("Number of Contours found = " + str(len(contours)))
    # cv2.drawContours(frame, contours[0], -1, (0, 255, 0), 3)
    # cv2.imshow('Contours', contours[1])
    # cv2.waitKey(0)
    x = [float(i[0][0])*2 for i in image_points]
    y = [float(i[0][1])*2 for i in image_points]
    # # make a box
    # x = list(range(0,1000,100)) + [1000]*10 + list(range(1000,0,-100)) + [0]*10
    # y = [0]*10 + list(range(0,1000,100)) + [1000]*10 + list(range(1000,0,-100))
    print(x)
    print(y)
    cv2.destroyAllWindows()
    points = []
    info_instruction = ins.Instruction()
    # Generate list of lists as instruction.instruct object
    for i in range(0, len(x)):
      points.append([x[i], y[i]])
    info_instruction.instruct = points
    # Two options based on system
    if raspberry_pi:
      self.ScALP_display.display_single_instruction(instruct=info_instruction.instruct, display_time=5)
    else:
      print("Not connected to ScALP system, plotting")
      self.ScALP_display.plot_single_instruction(instruct=info_instruction.instruct)


  def do_image(self, arg):
    """
    Reads image, creates point list for image, projects
    """
    img_name = input("Provide file name with extension: ")
    file = "./media/" + img_name
    print(file)
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = 100
    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    thresh_img = cv2.bitwise_not(img_grey)
    contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours[0] is a list of all the contours with points for each
    ctour_points = contours[0]
    # From this list of contours, isolate the longest one (most points)
    ctour_of_interest_index = self.ScALP_frame.get_index_of_longest_contour(ctours=contours)
    # Find a list of 50 equally spaced points along the longest contours in the image
    ctour_points_equally_spaced = self.ScALP_frame.convert_instruction_to_equal_spacing(contour_points=ctour_points[ctour_of_interest_index])
    image_instruction = ins.Instruction()
    image_instruction.instruct = ctour_points_equally_spaced
    # Two options based on system
    if raspberry_pi:
      self.ScALP_display.display_single_instruction(instruct=image_instruction.instruct, display_time=5)
    else:
      print("Not connected to display, plotting")
      self.ScALP_display.plot_single_instruction(instruct=image_instruction.instruct)


  def do_video(self, arg):
    """
    Reads video, creates point list for each frame, projects
    """
    # Get video file
    video_name = "out.mp4"#input("Provide file name with extension: ")
    file_dir = "./media/" + video_name
    print("Analyzing video file: {}".format(file_dir))
    # Convert video to series of instructions for laser system
    # Step 1: frame by frame, cut video into jpgs and save to current_video _frames
    self.ScALP_frame.set_current_video_frame_diffs(video_location=file_dir)
    # Step 2: frame by frame, get diffs between frames and convert into threshs
    self.ScALP_frame.set_current_video_frame_threshs()
    video_instruction_series = self.ScALP_frame.get_instruction_series_from_video_frames(threshs_directory="./current_video_frame_threshs/")
    # print(video_instruction_series)
    scalp_instruction_set = ins.Instruction()
    scalp_instruction_set.instruct = video_instruction_series
    # print(scalp_instruction_set.instruct[1])
    if raspberry_pi:
      self.ScALP_display.display_series_of_instructions(instruct_series=scalp_instruction_set.instruct, display_time=1)
    else:
      print("Not connected to display, plotting")
      self.ScALP_display.plot_series_of_instructions(instruct_series=scalp_instruction_set.instruct)


  def do_threshold(self, arg):
    """
    Test limits of the laser projection
    """
    print("Testing limits")
    scalp_limit_and_color_instruction = ins.Instruction()
    bounding_box_and_cross_instruction = [[0, 0], [1000, 1000], [1000, 0], [0, 1000], 
      [0, 0], [1000, 0], [1000, 1000], [0, 1000]]
    scalp_limit_and_color_instruction.instruct = bounding_box_and_cross_instruction
    if raspberry_pi:
      self.ScALP_display.display_single_instruction(instruct=scalp_limit_and_color_instruction.instruct, display_time=5)
    else: 
      print("Not connected to display, plotting instruction")
      self.ScALP_display.plot_single_instruction(instruct=scalp_limit_and_color_instruction.instruct)


  def do_message(self, arg):
    """
    Write a string of characters
    """
    scalp_ms = ms.Message()
    scalp_ms.get_message()
    scalp_message_instruction = ins.Instruction()
    scalp_message_instruction.instruct = scalp_ms.message_instuction
    if raspberry_pi:
      self.ScALP_display.display_single_instruction(instruct=scalp_message_instruction.instruct, display_time=5)
    else: 
      print("Not connected to display, plotting instruction message")
      self.ScALP_display.plot_single_instruction(instruct=scalp_message_instruction.instruct)


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


if __name__ == '__main__':
  c = ScALP()
  c.cmdloop()
  sys.exit()
