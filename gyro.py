import utime
from machine import I2C, Pin
from mpu6500 import MPU6500
import math


class Gyro:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        self.sensor = MPU6500(self.i2c)
   
    def start(self):
        print("MPU9250 id: " + hex(self.sensor.whoami))
        while True:
            data = self.sensor.gyro
            yaw, pitch, roll = self.get_yaw_pitch_roll(data)
            print("Yaw:", yaw)
            print("Pitch:", pitch)
            print("Roll:", roll)
            utime.sleep_ms(100)

    def print_column(self, column):
        if column == "YAW":
            index = 0
        elif column == "PITCH":
            index = 1
        else:  # assume column == "ROLL"
            index = 2
        
        print(f"{column}:")
        while True:
            data = self.sensor.gyro
            print(data[index])
            utime.sleep_ms(1000)

    def get_yaw_pitch_roll(self, gyro_data):
        gyro_data_deg = [math.degrees(val) for val in gyro_data]
        yaw = gyro_data_deg[0]
        pitch = gyro_data_deg[1]
        roll = gyro_data_deg[2]

        # Ensure the values are in the range -180 to 180
        yaw = self.normalize_angle(yaw)
        pitch = self.normalize_angle(pitch)
        roll = self.normalize_angle(roll)

        return yaw, pitch, roll

    def normalize_angle(self, angle):
        while angle > 180:
            angle -= 360
        while angle <= -180:
            angle += 360
        return angle