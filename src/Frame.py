# The Frame class is for generating contours and 
# instructions for single frame photos and images

import os
import cv2
import numpy as np
from src import Instruction as ins
from src import Display as disp

class Frame:

  def __init__(self):
    self.count = 0
    self.test_display = disp.Display()


  def blur_boundary_of_image(self, img_to_blur):
    """
    :param img: cv2 image read format
    Returns output image with Gaussian blurred edges
    """
    # img = cv2.imread("./media/lena.png")
    img_shape = np.shape(img_to_blur)
    img_x_width = img_shape[0]
    img_y_height = img_shape[1]
    img_x_middle = int(round(img_x_width/2))
    img_y_middle = int(round(img_y_height/2))
    print(img_shape)
    print(type(img_shape))
    blurred_img = cv2.GaussianBlur(img_to_blur, (21, 21), 0)

    mask = np.zeros((img_x_width, img_y_height, 3), dtype=np.uint8)
    mask = cv2.circle(mask, (img_x_middle, img_y_middle), 100, (255, 255, 255), -1)

    out_img = np.where(mask, img_to_blur, blurred_img)
    cv2.imwrite("./out.png", out_img)
    return out_img


  def get_contour_of_image(self, image_path):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Difference in color gradient, affects contour determination
    thresh = 150
    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # img_contours = np.zeros(img_grey.shape)
    # cv2.imwrite('./contours.png',img_contours)
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
    new_ins = ins.Instruction()
    new_ins.instruct = np.asarray(a=new_instruction_list)
    return new_ins, np.asarray(a=new_instruction_list)


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
          xs.append(i[0][0])
          ys.append(i[0][1])
      # closed contour from xc and yc
      xc = xs + [xs[0]]
      yc = ys + [ys[0]]
      # spacing between points
      dx = np.diff(xc)
      dy = np.diff(yc)
      dS = np.sqrt(dx*dx + dy*dy)
      dS = [0] + list(dS)
      d = np.cumsum(dS)
      perimeter = d[-1]
      N = 100
      ds = perimeter / N
      dSi = [ds*i for i in range(0, N)]
      # xi = []
      # yi = []
      # dSi[-1] = dSi[-1] - 0.005
      xi = np.interp(dSi, d, xc)
      yi = np.interp(dSi, d, yc)
      instruction_list_format = []
      for count, element in enumerate(xi, 0):
          instruction_list_format.append([xi[count], yi[count]])
      return instruction_list_format


  def get_index_of_longest_contour(self, ctours):
    # Given contours object, returns index of contours[0] that is longest
    index = 0
    longest_ct = 1
    for count, ct in enumerate(ctours[0], 0):
      ct_len = len(ct)
      if ct_len > longest_ct:
        longest_ct = ct_len
        index = count
    return index


  def set_current_video_frame_diffs(self, video_location: str):
    capture = cv2.VideoCapture(video_location)
    count = 0
    for i in range(200):
      ret1, frame1 = capture.read()
      ret2, frame2 = capture.read()
      try:
        frame_diff = frame2 - frame1
        # cv2.imshow("example diff", frame_diff)
        cv2.imwrite("./current_video_frame_diffs/frame_d%d.jpg" % count, frame_diff)
      except:
        print("Diff did not compute for frame: {}".format(i))
      count += 1
      if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    capture.release()
    cv2.destroyAllWindows() # destroy all opened windows
  

  def set_current_video_frame_threshs(self):
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


  def get_instruction_series_from_video_frames(self, threshs_directory):
    video_instruction_series = []
    # grab all files in directory
    files = os.listdir(threshs_directory)
    # sort by number on end of filename
    files = sorted(files,key=lambda x: int(os.path.splitext(x[7:])[0]))
    img_files = list(filter(lambda x: '.jpg' in x, files))
    # For each image in the folder, find and store the longest contour
    for img in img_files:
      path = threshs_directory + img
      img_read = cv2.imread(path)
      img_grey = cv2.cvtColor(img_read, cv2.COLOR_BGR2GRAY)
      contours = cv2.findContours(img_grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      ctour_points = contours[0]

      # last_element_index = len(contours)-1
      # contours = contours[:last_element_index]
      # Return largest contour found
      # contour_count = 0
      # longest_contour = 0
      # len_longest_contour = 0
      # for contour in contours:
      #   if len(contour[0]) > len_longest_contour:
      #     longest_contour = contour_count
      #     len_longest_contour = len(contour[0])
      #   contour_count += 1
      # l_contour = contours[longest_contour]

      longest_contour = self.get_index_of_longest_contour(ctours=contours)
      l_contour = self.convert_instruction_to_equal_spacing(contour_points=ctour_points[longest_contour])

      # frame_instruction_series = l_contour[:, :2]
      # print(frame_instruction_series[0])
      self.test_display.plot_single_instruction(instruct=l_contour)
      video_instruction_series.append(l_contour)
    return video_instruction_series