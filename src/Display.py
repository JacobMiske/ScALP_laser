# The Display class is handed Instructions and sends necessary 
# commands to the laser controller over a SPI bus
import time

raspberry_pi = False

if raspberry_pi:
    import spidev
    spi1 = spidev.SpiDev()
    spi1.open(0,1)
    spi1.max_speed_hz = 250000
    spi1.bits_per_word = 8
    spi1.mode = 0
    spi2 = spidev.SpiDev(0, 1)
    spi2.max_speed_hz = 250000

class Display:

    def __init__(self) -> None:
        pass

    def display_instruction(self, instruct, display_time):
        # Given single instruction, display for $display_time seconds
        if raspberry_pi:
            x = list(instruct[:, 0])
            y = list(instruct[:, 1])
            t_end = time.time() + display_time
            while time.time() < t_end:
                for count, point in enumerate(x, 0):
                    x_val = int(x[count]) + 4096
                    x_b_val = f'{x_val:016b}'
                    hex1 = hex(int(x_b_val[0:8], 2))
                    hex2 = hex(int(x_b_val[8:16], 2))
                    hex1 = int(hex1, 16)
                    hex2 = int(hex2, 16)
                    spi1.writebytes([hex1, hex2])
                    y_val = int(y[count]) + 36864
                    y_b_val = f'{y_val:016b}'
                    hex1 = hex(int(y_b_val[0:8], 2))
                    hex2 = hex(int(y_b_val[8:16], 2))
                    hex1 = int(hex1, 16)
                    hex2 = int(hex2, 16)
                    spi1.writebytes([hex1, hex2])
        else:
            print("System is not setup to run Display functions")
            return -1