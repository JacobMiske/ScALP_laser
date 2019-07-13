'''
This is a test script for observing Canny edge detection.

It will loop and persist a feed of black and white bitmaps.
'''

import time
import cv2
import numpy as np
from matplotlib import pyplot as plt

while True:
    vidcap = cv2.VideoCapture()         # Open webcam
    vidcap.open(0)
    retval, image = vidcap.retrieve()   # Save webcam pic
    time.sleep(0.)
    vidcap.release()                    # Clear webcam
    cv2.imwrite("test2.png", image)
    img = cv2.imread('test2.png',0)
    edges = cv2.Canny(img,100,200)
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.savefig('messi5_edge.png')
    plt.show()
    time.sleep(0.01)
