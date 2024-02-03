from machine import Pin
import utime

# kp, ki, kd - эти коэффициенты необходимо будет задать, а затем подстроить
# dt - времzя, т.е как часто будет пересчитываться П.И.Д
# minOut, maxOut - ограничение выхода

class PIDController:
    def __init__(self, kp, ki, kd, dt, minOut, maxOut):
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self.dt = dt
        self.minOut = minOut
        self.maxOut = maxOut
        self.prevErr = 0
        self.integral = 0

    @property
    def kp(self):
        return self._kp

    @kp.setter
    def kp(self, value):
        self._kp = value

    @property
    def ki(self):
        return self._ki

    @ki.setter
    def ki(self, value):
        self._ki = value

    @property
    def kd(self):
        return self._kd

    @kd.setter
    def kd(self, value):
        self._kd = value

    def set_coefficients(self, kp, ki, kd):
        self._kp = kp
        self._ki = ki
        self._kd = kd

    def reset(self):
        self.prevErr = 0
        self.integral = 0

    def log_values(self):
        print(f"PrevErr: {self.prevErr}, Integral: {self.integral}")

    def compute(self, input, setpoint):
        err = setpoint - input
        self.integral = self._constrain(self.integral + err * self.dt * self._ki, self.minOut, self.maxOut)
        D = (err - self.prevErr) / self.dt
        self.prevErr = err
        output = err * self._kp + self.integral + D * self._kd
        return self._constrain(output, self.minOut, self.maxOut)

    def _constrain(self, value, minVal, maxVal):
        if value < minVal:
            return minVal
        elif value > maxVal:
            return maxVal
        else:
            return value