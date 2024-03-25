from machine import Pin, PWM
import math

class L298N_motor:
    def __init__(self, EN1, IN1_1,EN2, IN2_1):
        self.ENA = PWM(Pin(EN1))
        self.IN1_1 = Pin(IN1_1, mode=Pin.OUT)
        self.ENB = PWM(Pin(EN2))
        self.IN2_1 = Pin(IN2_1, mode=Pin.OUT)
        self.speed = 0

    def setDirection(self, dir_1, dir_2):
        if dir_1 is 0:
            sp_1 = 100
        elif dir_1 is 2:
            sp_1 = -100
        else:
            sp_1 = 0
                
        if dir_2 is 0:
            sp_2 = 100
        elif dir_2 is 2:
            sp_2 = -100
        else:
            sp_2 = 0
        self.setSpeed(sp_1,sp_2)

    def setSpeed(self, speed_1, speed_2):
        self.ENA.freq(50)
        self.ENB.freq(50)
        speed_1 = min(100, max(-100, speed_1))
        speed_2 = min(100, max(-100, speed_2))
        if speed_1 > 0:
            self.IN1_1.value(1)
        elif speed_1 < 0:
            self.IN1_1.value(0)
        else:
            self.IN1_1.value(0)
        
        if speed_2 > 0:
            self.IN2_1.value(1)
        elif speed_1 < 0:
            self.IN2_1.value(0)
        else:
            self.IN2_1.value(0)

        self.ENA.duty_u16(int(math.fabs(speed_1)/100*65536))
        self.ENB.duty_u16(int(math.fabs(speed_2)/100*65536))

    def close(self):
        self.ENA.deinit()
        self.ENB.deinit()

