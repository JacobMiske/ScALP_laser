import matplotlib.pyplot as plt

class Instruction:

    def __init__(self, instruct):
        self.instruct = instruct
        self.instruct_first_x = list(instruct[0][0])
        self.instruct_first_y = list(instruct[0][1])

    def get_instruction_sizes(self):
        print("Number of instructions: ")
        print(len(self.instruct))

    def get_instruction_lengths(self):
        for count, instruction in enumerate(self.instruct, 0):
            print("Instruction set %d x and y lengths", count)
            print(len(instruction[0]))
            print(len(instruction[1]))
    
    def plot_first_instruction(self):
        plt.figure(100)
        plt.scatter(self.instruct_first_x, self.instruct_first_y)
        plt.savefig("first_instruction.jpg")
        plt.close
