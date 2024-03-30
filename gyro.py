"""
GyroscopeDataLogger class for Raspberry Pi Pico using MPU6500 sensor.
This class provides orientation estimation using a complementary filter.
"""
from machine import I2C, Pin
from mpu9250 import MPU9250
from time import sleep
from math import sqrt, atan2, degrees, sin, cos, pi

class GyroscopeDataLogger:
    def __init__(self):
        """
        Initialize the GyroscopeDataLogger class.
        """
        MPU = 0x68
        id = 1
        sda = Pin(26)
        scl = Pin(27)
        self.i2c = I2C(id=id, scl=scl, sda=sda, freq=400000)
        # Создание экземпляра MPU9250 для работы с датчиком
        self.mpu = MPU9250(self.i2c)
        # Начальные углы крена, тангажа и рыскания (pitch, roll, yaw)
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw_gyro = 0.0
        self.yaw_mag = 0.0
        # Константы для комплементарного фильтра
        self.alpha = 0.98
        self.dt = 0.01  # Шаг времени в секундах
        # Параметры для калибровки
        self.gyro_bias = [0.0, 0.0, 0.0]
        self.accel_bias = [0.0, 0.0, 0.0]
        self.mag_bias = [0.0, 0.0, 0.0]
        self.mag_scale = [1.0, 1.0, 1.0]
        self.calibrate()
        self.calibrate_range()

    def calibrate(self):
        """
        Calibrate the gyroscope, accelerometer, and magnetometer.
        """
        print("Calibrating... Keep the sensor still.")
        num_samples = 1000
        gyro_sum = [0.0, 0.0, 0.0]
        accel_sum = [0.0, 0.0, 0.0]
        mag_min = [0.0, 0.0, 0.0]
        mag_max = [0.0, 0.0, 0.0]

        # Сбор образцов для калибровки
        for _ in range(num_samples):
            gyro_data = self.mpu.gyro
            accel_data = self.mpu.acceleration
            mag_data = self.mpu.magnetic

            for i in range(3):
                gyro_sum[i] += gyro_data[i]
                accel_sum[i] += accel_data[i]
                if mag_data[i] < mag_min[i]:
                    mag_min[i] = mag_data[i]
                if mag_data[i] > mag_max[i]:
                    mag_max[i] = mag_data[i]

            sleep(0.005)

        # Расчет смещений и масштабов для калибровки
        for i in range(3):
            self.gyro_bias[i] = gyro_sum[i] / num_samples
            self.accel_bias[i] = accel_sum[i] / num_samples
            self.mag_bias[i] = (mag_max[i] + mag_min[i]) / 2.0
            self.mag_scale[i] = (mag_max[i] - mag_min[i]) / 2.0

        print("Calibration done.")
        print("Gyro Bias:", self.gyro_bias)
        print("Accel Bias:", self.accel_bias)
        print("Mag Bias:", self.mag_bias)
        print("Mag Scale:", self.mag_scale)

    def calibrate_range(self):
        """
        Calibrate gyroscope to measure full range of angles.
        """
        print("Calibrating range... Rotate the sensor to cover all angles.")

        # Инициализация переменных для хранения минимальных и максимальных значений углов
        min_pitch, max_pitch = float('inf'), -float('inf')
        min_roll, max_roll = float('inf'), -float('inf')
        min_yaw, max_yaw = float('inf'), -float('inf')

        # Сбор образцов для калибровки
        num_samples = 5000
        for _ in range(num_samples):
            pitch, roll, yaw = self.get_orientation()
            min_pitch = min(min_pitch, pitch)
            max_pitch = max(max_pitch, pitch)
            min_roll = min(min_roll, roll)
            max_roll = max(max_roll, roll)
            min_yaw = min(min_yaw, yaw)
            max_yaw = max(max_yaw, yaw)
            sleep(0.005)

        # Обновление значений для диапазона углов
        self.min_pitch = min_pitch
        self.max_pitch = max_pitch
        self.min_roll = min_roll
        self.max_roll = max_roll
        self.min_yaw = min_yaw
        self.max_yaw = max_yaw

        print("Range calibration done.")
        print("Pitch range: [{}, {}]".format(self.min_pitch, self.max_pitch))
        print("Roll range: [{}, {}]".format(self.min_roll, self.max_roll))
        print("Yaw range: [{}, {}]".format(self.min_yaw, self.max_yaw))


    def update_orientation(self):
        """
        Update orientation using complementary filter.
        """
        gx, gy, gz = [g - bias for g, bias in zip(self.mpu.gyro, self.gyro_bias)]
        ax, ay, az = [a - bias for a, bias in zip(self.mpu.acceleration, self.accel_bias)]
        mx, my, mz = [(m - bias) / scale for m, bias, scale in zip(self.mpu.magnetic, self.mag_bias, self.mag_scale)]

        # Расчет углов от гироскопа
        self.pitch += gx * self.dt
        self.roll -= gy * self.dt
        self.yaw_gyro += gz * self.dt
        
        # Коррекция углов по акселерометру
        accel_roll = atan2(ay, az)
        accel_pitch = atan2(-ax, sqrt(ay**2 + az**2))

        # Применение комплементарного фильтра
        self.pitch = self.alpha * self.pitch + (1 - self.alpha) * accel_pitch 
        self.roll = self.alpha * self.roll + (1 - self.alpha) * accel_roll
        
        # Расчет yaw по магнитометру
        Yh = (my * cos(self.roll)) - (mz * sin(self.roll))
        Xh = (mx * cos(self.pitch)) + (my * sin(self.roll) * sin(self.pitch)) + (mz * cos(self.roll) * sin(self.pitch))
        self.yaw_mag = atan2(Yh, Xh)
        
        # Применение комплементарного фильтра к углам yaw
        self.yaw = self.alpha * self.yaw_gyro + (1 - self.alpha) * self.yaw_mag
        
        # Ограничение yaw в диапазоне от -180 до 180 градусов
        if self.yaw > pi:
            self.yaw -= 2 * pi
        elif self.yaw < -pi:
            self.yaw += 2 * pi


    def get_heading(self):
        """
        Get heading in degrees.
        """
        self.update_orientation()
        heading = degrees(self.yaw)
        # Приведение угла к диапазону от 0 до 360
        if heading < 0:
            heading += 360
        return heading

    def get_direction(self, heading):
        """
        Get direction based on heading.
        """
        # Определение направления в зависимости от угла
        if 22.5 <= heading < 67.5:
            return "Northeast"
        elif 67.5 <= heading < 112.5:
            return "East"
        elif 112.5 <= heading < 157.5:
            return "Southeast"
        elif 157.5 <= heading < 202.5:
            return "South"
        elif 202.5 <= heading < 247.5:
            return "Southwest"
        elif 247.5 <= heading < 292.5:
            return "West"
        elif 292.5 <= heading < 337.5:
            return "Northwest"
        else:
            return "North"

    def get_orientation(self):
        """
        Get pitch, roll, and yaw in degrees.
        """
        self.update_orientation()
        # Приведение углов к диапазону от -180 до 180
        pitch = degrees(self.pitch)
        roll = degrees(self.roll)
        yaw = degrees(self.yaw)
        if pitch > 180:
            pitch -= 360
        if roll > 180:
            roll -= 360
        if yaw > 180:
            yaw -= 360
        return pitch, roll, yaw

if __name__ == "__main__":
    gyro = GyroscopeDataLogger()
    while True:
        pitch, roll, yaw = gyro.get_orientation()
        heading = gyro.get_heading()
        direction = gyro.get_direction(heading)
        print("Pitch:", round(pitch), "Roll:", round(roll), "Yaw:", round(yaw))
        print("Heading:", round(heading), "degrees, Direction:", direction)
        sleep(0.05)