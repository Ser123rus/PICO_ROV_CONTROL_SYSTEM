"""
GyroscopeDataLogger class for Raspberry Pi Pico using MPU6500 sensor.
This class provides orientation estimation using a complementary filter.
"""
from machine import I2C, Pin
from mpu6500 import MPU6500
from time import sleep, ticks_ms
from math import sqrt, atan2, pi, cos, sin, degrees

class GyroscopeDataLogger:
    def __init__(self):
        """
        Initialize the GyroscopeDataLogger class.
        """
        MPU = 0x68
        id = 1
        sda = Pin(26)
        scl = Pin(27)
        # create the I2C
        self.i2c = I2C(id=id, scl=scl, sda=sda)
        # Scan the bus
        print(self.i2c.scan())
        self.mpu = MPU6500(self.i2c)
        # Calibration and bias offset
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        # Constants for complementary filter
        self.alpha = 0.98
        self.dt = 0.01  # time step in seconds
        # Calibration data
        self.gyro_bias = [0.0, 0.0, 0.0]
        self.accel_bias = [0.0, 0.0, 0.0]
        self.calibrate()

    def calibrate(self):
        """
        Calibrate the gyroscope and accelerometer biases.
        """
        print("Calibrating... Keep the sensor still.")
        num_samples = 1000
        gyro_sum = [0.0, 0.0, 0.0]
        accel_sum = [0.0, 0.0, 0.0]

        for _ in range(num_samples):
            gyro_data = self.mpu.gyro
            accel_data = self.mpu.acceleration

            for i in range(3):
                gyro_sum[i] += gyro_data[i]
                accel_sum[i] += accel_data[i]

            sleep(0.005)

        for i in range(3):
            self.gyro_bias[i] = gyro_sum[i] / num_samples
            self.accel_bias[i] = accel_sum[i] / num_samples

        print("Calibration done.")
        print("Gyro Bias:", self.gyro_bias)
        print("Accel Bias:", self.accel_bias)

    def update_orientation(self):
        """
        Update orientation using complementary filter.
        """
        # получаем в 69-й строке данные гироскопа, в 70-й получаем с акселерометра
        gx, gy, gz = [g - bias for g, bias in zip(self.mpu.gyro, self.gyro_bias)]
        ax, ay, az = [a - bias for a, bias in zip(self.mpu.acceleration, self.accel_bias)]

        # Calculate angles from gyroscope
        self.pitch += gx * self.dt
        self.roll -= gy * self.dt
        self.yaw += gz * self.dt #yaw не ограничена, изменяется больше чем -180 180,
        # yaw в дальнейшем не согласовывается с акселерометром, просто ось Z
        
        # Correct angles using accelerometer
        accel_roll = atan2(ay, az)
        accel_pitch = atan2(-ax, sqrt(ay**2 + az**2))

        # тут комплиментарный фильтр, для того чтобы склеить гироскоп с акселерометром
        self.pitch = self.alpha * self.pitch + (1 - self.alpha) * accel_pitch 
        self.roll = self.alpha * self.roll + (1 - self.alpha) * accel_roll

    def show(self):
        """
        Display pitch, roll, and yaw angles in degrees.
        """
        self.update_orientation()
        print("Pitch:", round(degrees(self.pitch)), "Roll:", round(degrees(self.roll)), "Yaw:", round(degrees(self.yaw)))
        sleep(0.01)
        res = [round(degrees(self.pitch)), round(degrees(self.roll)), round(degrees(self.yaw))]
        return res

if __name__ == "__main__":
    gyro = GyroscopeDataLogger()
    while True:
        gyro.show()