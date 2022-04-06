# The Instruction class holds info of a single instruction or series of 
# instructions to be displayed by the Display object
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Instruction:

    def __init__(self):
        self.name = ""
        # Singular instruction
        self.instruct = []
        # Multiple instruction
        self.instruction_series = []


    def __str__(self):
        return str(self.instruct)


    def get_instruction_size(self):
        print("Number of points in single instruction: ")
        print(len(self.instruct))
        print("Number of instructions in instruction series: ")
        print(len(self.instruction_series))
    

    def get_instruction_series_from_video_frames(self, directory):
        instruction_set = []
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
        plt.figure(1)
        plt.scatter(self.instruct[:, 0], self.instruct[:, 1])
        plt.xlim([0, 1200])
        plt.ylim([0, 1200])
        plt.savefig("./instruction_plots/instruction.png")
        plt.close
    

    def plot_instruction_series(self):
        for count, instruct in enumerate(self.instruction_series, 0):
            plt.figure(count)
            plt.figure(100)
            plt.scatter(instruct[0][:, 0], instruct[0][:, 1])
            plt.xlim([0, 1200])
            plt.ylim([0, 1200])
            plt.savefig("./instruction_plots/instruction_plot_{}.jpg".format(count))
            plt.close()