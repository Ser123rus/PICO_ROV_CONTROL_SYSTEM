import utime
from machine import I2C, Pin
from mpu6500 import MPU6500

class Gyro:
    def __init__(self):
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.sensor = MPU6500(self.i2c)

    def start(self):
        print("MPU9250 id: " + hex(self.sensor.whoami))

        while True:
            data = self.sensor.gyro
            print("X:", data[0])
            print("Y:", data[1])
            print("Z:", data[2])
            utime.sleep_ms(1000)

    def print_column(self, column):
        if column == "X":
            index = 0
        elif column == "Y":
            index = 1
        else:  # assume column == "Z"
            index = 2
        
        print(f"{column}:")
        while True:
            data = self.sensor.gyro
            print(data[index])
            utime.sleep_ms(1000)
'''
gyro = Gyro()
gyro.start()
   '''     
    
