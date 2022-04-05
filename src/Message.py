# The Message class asks for inputs in text and generates
# an Instruction object to be passed to the Display object.

import cv2
import numpy as np
from data_structures.alphabet_dict import ALPHABET_DATA_FILE 

class Message:

    def __init__(self):
        self.message = ""

    def get_message(self):
        user_message = input("Please provide a short string of characters: ")
        print(user_message)