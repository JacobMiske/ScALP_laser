# The Instruction class holds info of a single instruction or series of 
# instructions to be displayed by the Display object
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Instruction:

    def __init__(self):
        self.name = ""
        # An instruct can either be:
        # Singular instruction, list of points in [x, y] 
        # format [[x1, y1], [x2, y2],...] OR
        # Multiple instruction, list of lists of points in [x, y]
        # format [[[x11, y11], [x12, y12],...], [[x21, y21], [x22, y22],...]]
        self.instruct = []
        # A color instruction series can either be:
        # Singular instruction, must be same length as self.instruct 
        # [color1, color2,...]
        # Multiple instruction, list of lists of colors
        # format [[[color11], [color12],...], [[color21], [color22],...],...]
        self.color_instruction_series = []


    def set_instruction_series(self, given_series):
        # directly sets the instruction series of the Instruction object
        self.instruct = given_series


    def set_color_instruction_series(self, given_color_series):
        # directly sets the color instruction series of the Instruction object
        self.color_instruction_series = given_color_series


    def __str__(self):
        return str(self.instruct)


    def get_instruction_size(self):
        print("Number of instructions in instruction series: ")
        print(len(self.instruct))
        print("Number of points in first instruction")
        print(len(self.instruct[0]))


    def append(self, point):
        # given a point, adds to end of self.instruct
        # point should be list with int X and Y -> [X, Y]
        self.instruct.append(point)
        return 0


    def plot_instruction(self):
        # For the first set of points in the instruction series, 
        plt.figure(1)
        plt.scatter(self.instruct[:, 0], self.instruct[:, 1])
        plt.xlim([0, 1200])
        plt.ylim([0, 1200])
        plt.savefig("./instruction_plots/instruction.png")
        plt.show(block=False)
        plt.pause(1) # show for 1 second
        plt.close("all")
    

    def plot_instruction_series(self):
        # For each individual set of points in the instruction series, plot and save
        for count, instruct in enumerate(self.instruct, 0):
            plt.figure(count)
            plt.figure(100)
            plt.scatter(instruct[0][:, 0], instruct[0][:, 1])
            plt.xlim([0, 1200])
            plt.ylim([0, 1200])
            plt.savefig("./instruction_plots/instruction_plot_{}.jpg".format(count))
            plt.show(block=False)
            plt.pause(1) # show for 1 second
            plt.close("all")
