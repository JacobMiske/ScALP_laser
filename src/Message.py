# The Message class asks for inputs in text and generates
# an Instruction object to be passed to the Display object.

import cv2
import numpy as np
from .data_structures.alphabet_dict import ALPHABET_DATA_FILE as ADF

class Message:

    def __init__(self):
        self.message = ""
        self.message_instruction = []

    def get_message(self):
        user_message = input("Please provide a short string of characters: ")
        self.message = user_message
        print(user_message)

    def get_instructions_for_text(self):
        # set list of instructions to pass into instruction object
        for char in self.message:
            print(ADF[char])
            self.message_instruction.append(ADF[char])
        pass 