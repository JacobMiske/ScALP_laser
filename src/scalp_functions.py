# Legacy code
import time
import cv2
import scipy.ndimage as ndimage

def bitstring_to_bytes(s):
  v = int(s, 2)
  b = bytearray()
  while v:
    b.append(v & 0xFF)
    v >>= 8
    return bytes(b[::-1])


def set_int_to_DAC():
    
  for i in range(17, 4000, 1):
    val = int(i) + 4096
    binary_val = f'{val:016b}'
    # hex_val = binToHexa(binary_val)
    res = bitstring_to_bytes(binary_val)
    hex1 = hex(int(binary_val[0:8], 2))
    print(hex1)
    print(type(hex1))
    hex2 = hex(int(binary_val[8:16], 2))
    print(type(int(hex2, 16)))
    print(type(0x30))
    hex1 = int(hex1, 16)
    hex2 = int(hex2, 16)
    spi1.writebytes([hex1, hex2])
    spi2.writebytes([hex1, hex2])
    time.sleep(0.005)
  
  for i in range(1000, 17, -1):
    val = int(i) + 12288
    binary_val = f'{val:016b}'
    # hex_val = binToHexa(binary_val)
    res = bitstring_to_bytes(binary_val)
    hex1 = hex(int(binary_val[0:8], 2))
    print(hex1)
    hex2 = hex(int(binary_val[8:16], 2))
    print(hex2)
    #spi1.writebytes([hex1, hex2])
    time.sleep(0.005)
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