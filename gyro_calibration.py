import utime

class GyroCalibration:
    def __init__(self, gyro):
        self.gyro = gyro
        self.calibrated = False

    def calibrate(self):
        print("Calibrating gyro...")
        sum_data = [0, 0, 0]
        num_samples = 100

        for _ in range(num_samples):
            raw_data = self.gyro.sensor.gyro
            sum_data = [sum(x) for x in zip(sum_data, raw_data)]
            utime.sleep_ms(10)

        self.offsets = [x / num_samples for x in sum_data]
        self.calibrated = True
        print("Calibration complete")

    def get_calibrated_data(self):
        if not self.calibrated:
            raise ValueError("Gyro is not calibrated. Run calibrate() first.")

        raw_data = self.gyro.sensor.gyro
        calibrated_data = [x - offset for x, offset in zip(raw_data, self.offsets)]
        return calibrated_data