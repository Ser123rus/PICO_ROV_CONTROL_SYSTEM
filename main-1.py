import barometer, ethernet, srv, gyro, l298dcmotor
from array import *
import utime
from machine import Pin
from time import sleep
from l298dcmotor import L298N_motor

sp_1 = 0
sp_2 = 0
dir_1 = 0
dir_2 = 0
class robot():
    def __init__(self):
        #barometerR = barometer.MS5837_30BA(bus=1, scl_pinid=15, sda_pinid=14, i2c_freq=400000)
        #barometerR.init()
        # ip робота, порт, ip компа, порт, mosi_pinid, miso_pinid, sck_pinid, eth_cs_pinid, eth_reset_pinid
        # host ip:port    192.168.0.100:8080
        self.ethernetR = ethernet.EthernetW5500('192.168.1.177', 8080, "192.168.1.100", 8888, 19, 16, 18, 17, 20)
        self.ethernetR.get_mac_address()
        servo_pins = [10,11,12,13,14,15]
        self.thruster = []
        for i in range(6):
            print("Init motor " + str(i))
            self.thruster.append(srv.Servo(servo_pins[i],min_us=544.0,max_us=2400.0,min_deg=0.0,max_deg=180.0,freq=50))
            self.thruster[i].write(180)
            utime.sleep_ms(2000)
            self.thruster[i].write(90)
            utime.sleep_ms(1500)
        self.camServo = srv.Servo(5,min_us=544.0,max_us=2400.0,min_deg=0.0,max_deg=180.0,freq=50)
        self.camServo.write(180)
        utime.sleep_ms(2000)
        self.camServo.write(90)
        utime.sleep_ms(1500)
        self.gyroR = gyro.GyroscopeDataLogger()
        self.manipulator = L298N_motor(6,7,8,9) # ENA,IN1,ENB,IN2
        print("robot has initialized")
    
    def encodeString(self, input):
        res = array('b')
        for i in range(len(input)):
            input[i] = str(input[i])
            for j in range(0,len(input[i])):
                res.append(ord(input[i][j]))
            if len(input[i]) < 6:
                x = 6 - len(input[i])
                while x > 0:
                    res.append(0)
                    x = x-1
            else:
                res.append(0)
        print(res)
        return res
            
    def loop(self):
        print("Main loop started.")
        while(1):
            print('S')
            self.ethernetR.toSend = self.encodeString(self.gyroR.show())
            self.ethernetR.run()
            for i in range(6):
                self.thruster[i].write(self.ethernetR.result[i] + 2)
            self.manipulator.setDirection(int(self.ethernetR.result[6]), int(self.ethernetR.result[7]))
            #self.ethernetR.toSend = self.ethernetR.data # пример echo отправки данных
            print('F')
            
            
if __name__=="__main__":
    katran = robot()
    katran.loop()
    