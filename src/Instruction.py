import matplotlib.pyplot as plt

class Instruction:

    def __init__(self, instruct):
        # Singular instruction
        self.instruct = instruct
        # Multiple instruction
        self.instruction_series = []

    def __str__(self):
        return str(self.instruct)

    def get_instruction_sizes(self):
        print("Number of instructions: ")
        print(len(self.instruct))

    def get_instruction_lengths(self):
        for count, instruction in enumerate(self.instruct, 0):
            print("Instruction set {} x and y lengths".format(count))
            # print(len(instruction[0]))
            # print(len(instruction[1]))
    
    def plot_first_instruction(self):
        plt.figure(100)
        plt.scatter(self.instruct[0][0], self.instruct[0][1])
        plt.xlim([0, 1200])
        plt.ylim([0, 1200])
        plt.savefig("./instruction_plots/first_instruction.jpg")
        plt.close
    
    def plot_all_instructions(self):
        for count, ins_frame in enumerate(self.instruct, 0):
            plt.figure(count)
            plt.figure(100)
            plt.scatter(ins_frame[0], ins_frame[1])
            plt.xlim([0, 1200])
            plt.ylim([0, 1200])
            plt.savefig("./instruction_plots/instruction_plot_{}.jpg".format(count))
            plt.close()