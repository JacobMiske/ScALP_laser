import cv2
import numpy as np

class Message:

    def __init__(self):
        self.message = ""

    def get_message(self):
        user_message = input("Please provide a short string of characters: ")
        print(user_message)