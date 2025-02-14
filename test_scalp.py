# Jacob Miske
# This script is for running test functions
# on the laser projector hardware
# GPL License
#!/usr/bin/python3

from dis import dis
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
from src import Instruction as ins
from src import Frame as fr
from src import Display as disp


def main():
    print("ScALP test \n ---------")
    # create display object
    test_display = disp.Display()

    
    # This segment of code drives the laser to the bounds of the laser limits, draws a cross through the center, and varies the color of the laser
    print("Testing laser limits and color")
    scalp_limit_and_color_instruction = ins.Instruction()
    display_time = 5 # five seconds
    bounding_box_and_cross_instruction = [[0, 0], [1000, 0], [1000, 1000], [0, 1000], [500, 500], 
        [1000, 0], [1000, 1000], [500, 500], [0, 1000]]
    
    scalp_limit_and_color_instruction.instruct = bounding_box_and_cross_instruction
    test_display.display_single_instruction(instruct=scalp_limit_and_color_instruction.instruct, display_time=5)

    # This segment of code tests generating an Instruction with a single frame
    print("Testing static instruction")
    scalp_frame = fr.Frame()
    single_contour = scalp_frame.get_contour_of_image(image_path="./whitestar.jpg")
    scalp_instruction = ins.Instruction()
    scalp_instruction = scalp_frame.get_instruction_from_contour(contour=single_contour)
    scalp_instruction.plot_instruction()


    # This segment of code tests an Instruction with multiple frames
    print("Testing dynamic instruction")
    file_dir = "./current_video_frame_threshs/"
    if [f for f in os.listdir(file_dir) if not f.startswith('.')] == []:
        print("empty dir")
        get_frames_diff_from_video()
    else: 
        print("not empty")
    # instruction_set = get_contour_instructions_per_frame()
    scalp_instruction_set = ins.Instruction()
    scalp_instruction_set.get_instruction_series_from_video_frames(directory=file_dir)
    print(scalp_instruction_set.instruction_series[1])
    # scalp_instruction_set.instruction_series = instruction_set
    # scalp_instruction_set.get_instruction_size()
    # scalp_instruction_set.plot_instruction_series()
    A = scalp_instruction_set.instruction_series
    scalp_display = disp.Display()
    scalp_display.display_series_of_instructions(instruct_series=A, display_time=1)
    # set_instruction_for_video(instruct = instruction_set)


def get_frames_from_video():
    cap = cv2.VideoCapture("./media/ball.mp4")
    count = 0
    while cap.isOpened():
        ret,frame = cap.read()
        # cv2.imshow('window-name', frame)
        cv2.imwrite("./current_video_frames/frame%d.jpg" % count, frame)
        count = count + 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows() # destroy all opened windows
    return 0


def get_frames_diff_from_video():
    cap = cv2.VideoCapture("./media/ball.mp4")
    count = 0
    for i in range(200):
        ret1, frame1 = cap.read()
        ret2, frame2 = cap.read()
        try:
            frame_diff = frame2 - frame1
            # cv2.imshow("example diff", frame_diff)
            cv2.imwrite("./current_video_frame_diffs/frame_d%d.jpg" % count, frame_diff)
        except:
            print("frame did not compute")
        count += 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows() # destroy all opened windows
    frame_diff_directory = "./current_video_frame_diffs/"
    count = 0
    files = os.listdir(frame_diff_directory)
    files = sorted(files,key=lambda x: int(os.path.splitext(x[7:])[0]))
    img_files = list(filter(lambda x: '.jpg' in x, files))
    for f in img_files:
        print(f)
        image = cv2.imread(frame_diff_directory+str(f), cv2.IMREAD_COLOR)
        img_grey =  cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = 10
        ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
        # cv2.imshow("thresh test", thresh_img)
        cv2.imwrite("./current_video_frame_threshs/frame_d%d.jpg" % count, thresh_img)
        count += 1
    cv2.destroyAllWindows() # destroy all opened windows
    return 0
        

def set_current_video_frame_diffs():
    cap = cv2.VideoCapture("./media/ball.mp4")
    count = 0
    for i in range(200):
        ret1, frame1 = cap.read()
        ret2, frame2 = cap.read()
        try:
            frame_diff = frame2 - frame1
            # cv2.imshow("example diff", frame_diff)
            cv2.imwrite("./current_video_frame_diffs/frame_d%d.jpg" % count, frame_diff)
        except:
            print("frame did not compute")
        count += 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows() # destroy all opened windows


def set_current_video_frame_threshs():
    frame_diff_directory = "./current_video_frame_diffs/"
    count = 0
    files = os.listdir(frame_diff_directory)
    files = sorted(files,key=lambda x: int(os.path.splitext(x[7:])[0]))
    img_files = list(filter(lambda x: '.jpg' in x, files))
    for f in img_files:
        print(f)
        image = cv2.imread(frame_diff_directory+str(f), cv2.IMREAD_COLOR)
        img_grey =  cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = 10
        ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
        # cv2.imshow("thresh test", thresh_img)
        cv2.imwrite("./current_video_frame_threshs/frame_d%d.jpg" % count, thresh_img)
        count += 1
    return 0


def get_contour_instructions_per_frame():
    ct = 0
    file_dir = "./current_video_frame_threshs/"
    instruction_set = []
    files = sorted(os.listdir(file_dir))
    img_files = list(filter(lambda x: '.jpg' in x, files))
    for img in img_files:
        cpts = get_contour_points(image_path=img)
        plot_longest_contours_in_frame(c_points=cpts)
        x_vals, y_vals = get_scatter_points_equal_spacing_plot(contour_points=cpts[0][0], count=ct)
        instruction_set.append([x_vals, y_vals])
        ct += 1
        # TODO: change when 10 good instruction sets made
        if ct == 10:
            return instruction_set
    return instruction_set


def get_contour_points(image_path):
    path = "./current_video_frame_threshs/"+str(image_path)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    # cv2.imshow("test", img)
    img_grey = img #cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh = 150
    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours
    img_contours = np.zeros(img_grey.shape)
    return contours


def get_scatter_points_plot(contour_points):
    xs = []
    ys = []
    for i in contour_points:
        xs.append(i[0][0])
        ys.append(i[0][1])
    return 0


def get_scatter_points_equal_spacing_plot(contour_points, count):
    # convert list of points to ordered list of x and y
    # print(contour_points)
    if len(contour_points) < 2:
        return -1, -1
    xs = []
    ys = []
    for i in contour_points:
        xs.append(i[0][0])
        ys.append(i[0][1])
    # closed contour from xc and yc
    xc = xs + [xs[0]]
    yc = ys + [ys[0]]
    # spacing between points
    dx = np.diff(xc)
    dy = np.diff(yc)
    dS = np.sqrt(dx*dx + dy*dy)
    # print(dS)
    dS = [0] + list(dS)
    d = np.cumsum(dS)
    perimeter = d[-1]
    N = 50
    ds = perimeter / N
    dSi = [ds*i for i in range(0, N)]
    xi = []
    yi = []
    dSi[-1] = dSi[-1] - 0.005
    xi = np.interp(dSi, d, xc)
    yi = np.interp(dSi, d, yc)
    plt.figure(1)
    plt.scatter(yi, xi)
    plt.savefig("./current_video_contours/{}.jpg".format(count))
    return xi, yi


def plot_all_contours_in_frame(c_points):
    plt.figure(2)
    for contour in c_points[0]:
        xs = []
        ys = []
        print(contour)
        for i in contour:
            xs.append(i[0][0])
            ys.append(i[0][1])
        plt.scatter(xs, ys)
    return 0


def plot_longest_contours_in_frame(c_points):
    index = 0
    longest_len = 0
    for contour in c_points[0]:
        length = len(contour)
        if length > longest_len:
            longest_len = length
            index += 1
            break
        else:
            index += 1
    # show longest contour
    plt.figure()
    xs = []
    ys = []
    for i in c_points[0][index]:
        xs.append(i[0][0])
        ys.append(i[0][1])
    plt.scatter(xs, ys)
    plt.close()
    return 0


def get_circle_on_binary_2D_array(array_size, center, radius):
    """
    :param array_size: tuple of format (x, y)
    :param center: tuple of format (x, y)
    :param radius: integer
    Returns numpy array with circles of ones on background of zeros
    """
    center_x = center[0]
    center_y = center[1]
    temp_array = np.zeros(array_size)
    for i in range(array_size[0]):
        for j in range(array_size[1]):
            distance_to_ij = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            if distance_to_ij < radius:
                temp_array[i, j] = 1
    # cv2.imshow('circle test', temp_array)
    # cv2.waitKey(0)
    return temp_array


if __name__ == '__main__':
    main()
