from machine import Pin
import utime

# kp, ki, kd - эти коэффициенты необходимо будет задать, а затем подстроить
# dt - времzя, т.е как часто будет пересчитываться П.И.Д
# minOut, maxOut - ограничение выхода

class PIDController:
    def __init__(self, kp, ki, kd, dt, minOut, maxOut):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.minOut = minOut
        self.maxOut = maxOut
        self.prevErr = 0
        self.integral = 0

    # Так как функции constrain() нет в Micropython, то это её аналог
    # constrain() - исходник arduino IDE
    def constrain(self, value, minVal, maxVal):
        if value < minVal: return minVal
        elif value > maxVal: return maxVal
        else: return value

    def compute(self, input, setpoint):
        err = setpoint - input
        self.integral = self.constrain(self.integral + err * self.dt * self.ki, self.minOut, self.maxOut)
        D = (err - self.prevErr) / self.dt
        self.prevErr = err
        output = err * self.kp + self.integral + D * self.kd
        return self.constrain(output, self.minOut, self.maxOut)

        