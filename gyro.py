from machine import Pin, I2C
from mpu6500 import MPU6500
import math
import utime

class GyroscopeDataLogger:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        self.sensor = MPU6500(self.i2c)
        self.zero_position = (0, 0, 0)
        self.current_angle = (0, 0, 0)
        self.prev_time = utime.ticks_ms()

    def rad_to_degrees(self, angle_rad):
        return angle_rad * (180.0 / math.pi)

    def set_zero_position(self):
        print("Установка нулевого положения гироскопа...")
        utime.sleep(2)
        self.zero_position = self.sensor.gyro

    def complementary_filter(self, angle, rate, dt):
        alpha = 0.98  # Настройте параметр alpha для оптимальной работы фильтра
        angle_new = alpha * (angle + rate * dt) + (1 - alpha) * angle

        # Приводим угол к диапазону от -180 до 180 градусов
        angle_new = (angle_new + 180) % 360 - 180

        return angle_new
    
    def read_gyroscope_data(self):
        try:
            while True:
                current_time = utime.ticks_ms()
                dt = (current_time - self.prev_time) / 1000.0
                self.prev_time = current_time

                gyro_data = tuple(map(lambda x, y: x - y, self.sensor.gyro, self.zero_position))
                gyro_data_deg = tuple(map(self.rad_to_degrees, gyro_data))

                # Используем фильтр наклона для сглаживания данных
                self.current_angle = tuple(
                    self.complementary_filter(angle, rate, dt) for angle, rate in zip(self.current_angle, gyro_data_deg)
                )

                print("Current Angle (X, Y, Z):", self.current_angle)
                utime.sleep(0.1)  # Уменьшили задержку для более частого обновления
        except KeyboardInterrupt:
            print("Программа завершена.")

if __name__ == "__main__":
    gyroscope_logger = GyroscopeDataLogger()
    gyroscope_logger.set_zero_position()
    gyroscope_logger.read_gyroscope_data()
