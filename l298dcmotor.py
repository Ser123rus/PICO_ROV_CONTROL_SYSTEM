from machine import Pin, PWM

class DCMotor:
    def __init__(self, pin1, pin2, enable_pin, min_duty=750, max_duty=1023):
        self.pin1 = Pin(pin1, Pin.OUT)
        self.pin2 = Pin(pin2, Pin.OUT)
        self.enable_pin = PWM(Pin(enable_pin))
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.speed = 0

    def forward(self, speed):
        self.speed = max(0, min(100, speed))
        self.enable_pin.duty(self.duty_cycle(self.speed))
        self.pin1.value(0)
        self.pin2.value(1)

    def backward(self, speed):
        self.speed = max(0, min(100, speed))
        self.enable_pin.duty(self.duty_cycle(self.speed))
        self.pin1.value(1)
        self.pin2.value(0)

    def stop(self):
        self.enable_pin.duty(0)
        self.pin1.value(0)
        self.pin2.value(0)

    def duty_cycle(self, speed):
        return int(self.map(speed, 0, 100, self.min_duty, self.max_duty))

    def set_speed(self, speed):
        self.speed = max(0, min(100, speed))
        self.enable_pin.duty(self.duty_cycle(self.speed))

    def set_speed_range(self, min_speed, max_speed):
        self.min_duty = self.map(min_speed, 0, 100, 0, 1023)
        self.max_duty = self.map(max_speed, 0, 100, 0, 1023)

    def log_status(self):
        print(f"Speed: {self.speed}, Duty Cycle: {self.duty_cycle(self.speed)}")

    @staticmethod
    def map(value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
