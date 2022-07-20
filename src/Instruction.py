# The Instruction class holds info of a single instruction or series of 
# instructions to be displayed by the Display object
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Instruction:

    def __init__(self):
        self.name = ""
        # Instruction_series can either be:
        # Singular instruction, list of points in [x, y] 
        # format [[x1, y1], [x2, y2],...] OR
        # Multiple instruction, list of lists of points in [x, y]
        # format [[[x11, y11], [x12, y12],...], [[x21, y21], [x22, y22],...]]
        self.instruction_series = []
        # Color instruction series can either be:
        # Singular instruction, must be same length as self.instruction_series 
        # [color1, color2,...]
        # Multiple instruction, list of lists of colors
        # format [[[color11], [color12],...], [[color21], [color22],...],...]
        self.color_instruction_series = []


    def set_instruction_series(self, given_series):
        # directly sets the instruction series of the Instruction object
        self.instruction_series = given_series


    def set_color_instruction_series(self, given_color_series):
        # directly sets the color instruction series of the Instruction object
        self.color_instruction_series = given_color_series


    def __str__(self):
        return str(self.instruction_series)


    def get_instruction_size(self):
        print("Number of instructions in instruction series: ")
        print(len(self.instruction_series))
        print("Number of points in first instruction")
        print(len(self.instruction_series[0]))


    def append(self, point):
        # given a point, adds to end of self.instruction_series
        # point should be list with int X and Y -> [X, Y]
        self.instruction_series.append(point)
        return 0


    def get_instruction_series_from_video_frames(self, directory):
        # grab all files in directory
        files = os.listdir(directory)
        # sort by number on end of filename
        files = sorted(files,key=lambda x: int(os.path.splitext(x[7:])[0]))
        img_files = list(filter(lambda x: '.jpg' in x, files))
        # For each image in the folder, find and store the longest contour
        for img in img_files:
            path = directory + img
            img_read = cv2.imread(path)
            img_grey = cv2.cvtColor(img_read, cv2.COLOR_BGR2GRAY)
            contours = cv2.findContours(img_grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            last_element_index = len(contours)-1
            contours = contours[:last_element_index]
            # Return largest contour found
            contour_count = 0
            longest_contour = 0
            len_longest_contour = 0
            for contour in contours:
                if len(contour[0]) > len_longest_contour:
                    longest_contour = contour_count
                    len_longest_contour = len(contour[0])
                contour_count += 1
            l_contour = contours[longest_contour]
            l_contour = l_contour[0]
            self.instruction_series.append(l_contour[:, :2])
        return 0


    def plot_instruction(self):
        # For the first set of points in the instruction series, 
        plt.figure(1)
        plt.scatter(self.instruction_series[:, 0], self.instruction_series[:, 1])
        plt.xlim([0, 1200])
        plt.ylim([0, 1200])
        plt.savefig("./instruction_plots/instruction.png")
        plt.close
    

    def plot_instruction_series(self):
        # For each individual set of points in the instruction series, plot and save
        for count, instruct in enumerate(self.instruction_series, 0):
            plt.figure(count)
            plt.figure(100)
            plt.scatter(instruct[0][:, 0], instruct[0][:, 1])
            plt.xlim([0, 1200])
            plt.ylim([0, 1200])
            plt.savefig("./instruction_plots/instruction_plot_{}.jpg".format(count))
            plt.close()
