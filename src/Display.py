# The Display class is handed Instructions and sends necessary 
# commands to the laser controller over a SPI bus
import time
from typing import final
import numpy as np
import matplotlib.pyplot as plt

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


class Display:


    def __init__(self):
        # Default display color is bright red
        self.color = [256, 0, 0]


    def display_single_instruction(self, instruct, display_time, color_list=None):
        # Given single instruction, display for $display_time seconds
        x = [item[0] for item in instruct]
        y = [item[1] for item in instruct]        
        try:
            if raspberry_pi:
                # If color_list = None, use default color for all points
                t_end = time.time() + display_time
                while time.time() < t_end:
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
            else:
                print("System is not setup to run Display functions")
                print("Showing plot of projected results")
                plt.figure(1)
                plt.plot(x, y)
                plt.show(block=False)
                plt.pause(1) # show for 1 second
                plt.close("all")
        except:
            print("Error in frame display function")
        finally: 
            return 0


    def display_series_of_instructions(self, instruct_series, display_time):
        """
        
        """
        try:
            if raspberry_pi:
                for instruct in instruct_series:
                    x = list(instruct[0][:, 0])
                    y = list(instruct[0][:, 1])
                    t_end = time.time() + display_time
                    while time.time() < t_end:
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
            else:
                # Get first frame xs and ys
                x = [item[0] for item in instruct_series[0]]
                y = [item[1] for item in instruct_series[0]]
                print("System is not setup to run Display functions")
                print("Showing plot of first frame")
                plt.figure(1)
                plt.plot(x, y)
                plt.show(block=False)
                plt.pause(1) # show for 1 second
                plt.close("all")
            return 0
        except:
            print("Error in series display function")
            return -1
        finally: 
            return 0


    def plot_single_instruction(self, instruct):
        # use array for easy indexing
        instruct = np.array(instruct)
        # X values as first column, Y values as second column
        x = list(instruct[:, 0])
        y = list(instruct[:, 1])
        plt.figure()
        plt.scatter(x, y)
        plt.show(block=False)
        plt.pause(1) # show for 1 second
        plt.close("all")


    def plot_series_of_instructions(self, instruct_series):
        """
        Show each frame for 1 second
        """
        for instruct in instruct_series:
            # use array for easy indexing
            instruct = np.array(instruct)
            # X values as first column, Y values as second column
            x = list(instruct[:, 0])
            y = list(instruct[:, 1])
            plt.figure()
            plt.scatter(x, y)
            plt.show(block=False)
            plt.pause(1) # show for 1 second
            plt.close("all")
