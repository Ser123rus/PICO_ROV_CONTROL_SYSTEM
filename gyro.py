from machine import I2C, Pin
from math import sqrt, atan2, pi, copysign, sin, cos
from mpu9250 import MPU9250
from time import sleep

class GyroscopeDataLogger:
    def __init__(self):
        MPU = 0x68
        id = 1
        sda = Pin(26)
        scl = Pin(27)
        # create the I2C
        self.i2c = I2C(id=id, scl=scl, sda=sda)
        # Scan the bus
        print(self.i2c.scan())
        self.m = MPU9250(self.i2c)
        # Calibration and bias offset
        self.pitch_bias = 0.0
        self.roll_bias = 0.0
        # For low pass filtering
        filtered_x_value = 0.0 
        filtered_y_value = 0.0
        # declination = 40
        x,y,z, pitch_bias, roll_bias = self.get_reading()

    def get_reading(self)->float:
        ''' Returns the readings from the sensor '''
        #global filtered_y_value, filtered_x_value
        x = self.m.acceleration[0] 
        y = self.m.acceleration[1]
        z = self.m.acceleration[2]
        print('x',x ,'y',y, 'z',z)

        # Pitch and Roll in Radians
        roll_rad = atan2(-x, sqrt((z*z)+(y*y)))
        pitch_rad = atan2(z, copysign(y,y)*sqrt((0.01*x*x)+(y*y)))
    
        # Pitch and Roll in Degrees
        pitch = pitch_rad*180/pi
        roll = roll_rad*180/pi
        
        # Adjust for original bias
        pitch -= self.pitch_bias
        roll -= self.roll_bias
    
        return x, y, z, pitch, roll

    def low_pass_filter(self, raw_value:float, remembered_value): # не используется 
        ''' Only applied 20% of the raw value to the filtered value '''
        
        # global filtered_value
        alpha = 0.8
        filtered = 0
        filtered = (alpha * remembered_value) + (1.0 - alpha) * raw_value
        return filtered
    
    def show(self):
        ''' Shows the Pitch, Rool and heading '''
        x, y, z, pitch, roll = self.get_reading()
        print("Pitch",round(pitch,1), "Roll",round(roll, 1))
        sleep(0.2)
        res = [round(pitch,1), round(roll, 1)]
        return res
    

if __name__ == "__main__":
    gyro = GyroscopeDataLogger()
    while True:
        gyro.show()
