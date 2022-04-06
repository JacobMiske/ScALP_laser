# The Frame class is for generating contours and 
# instructions for single frame photos and images

import cv2
import numpy as np
from src import Instruction as ins

class Frame:

    def __init__(self):
        self.count = 0

    def get_contour_of_image(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        thresh = 150
        ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
        contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_contours = np.zeros(img_grey.shape)
        cv2.imwrite('./contours.png',img_contours)
        # Return largest contour found
        contour_count = 0
        longest_contour = 0
        len_longest_contour = 0
        for contour in contours:
            if len(contour[0]) > len_longest_contour:
                longest_contour = contour_count
                len_longest_contour = len(contour[0])
            contour_count += 1
        return contours[longest_contour]

    def get_instruction_from_contour(self, contour):
        new_instruction_list = []
        array = contour[0]
        for point in array:
            x_val = point[0][0]
            y_val = point[0][1]
            new_instruction_list.append([x_val, y_val])
        new_instruction_list = self.convert_instruction_to_equal_spacing(contour_points=new_instruction_list)
        # print(new_instruction_list)
        new_ins = ins.Instruction()
        new_ins.instruct = np.asarray(a=new_instruction_list)
        return new_ins


    def set_frame(self):
        """
        Based on background, take short video with subject and run subtraction
        """
        cam = cv2.VideoCapture(0)
        if (cam.isOpened() == False): 
            print("Error reading video")
        frame_width = int(cam.get(3))
        frame_height = int(cam.get(4))
        size = (frame_width, frame_height)
        input("Press enter to take video with you in it")
        result = cv2.VideoWriter('./foreground_video.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
        for i in range(60):
            ret, frame = cam.read()
            if ret == True: 
                result.write(frame)
                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
            else:
                break
        capture = cv2.VideoCapture('./foreground_video.avi')
        frameIds = capture.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)
        frames = []
        for frame_id in frameIds:
            capture.set(cv2.CAP_PROP_FRAME_COUNT, frame_id)
            ret, frame = capture.read()
            frames.append(frame)
        median_frame = np.median(frames, axis=0).astype(dtype=np.uint8)
        cv2.imwrite('./foreground_frame.jpg', median_frame)
        cam.release()
        result.release()
        cv2.destroyAllWindows()

    def convert_instruction_to_equal_spacing(self, contour_points):
        xs = []
        ys = []
        for i in contour_points:
            xs.append(i[0])
            ys.append(i[1])
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
        instruction_list_format = []
        for count, element in enumerate(xi, 0):
            instruction_list_format.append([xi[count], yi[count]])
        return instruction_list_format
