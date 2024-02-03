import barometer, ethernet, srv, gyro, l298dcmotor
from array import *

class robot():
    def __init__(self):
        #barometerR = barometer.MS5837_30BA(bus=1, scl_pinid=15, sda_pinid=14, i2c_freq=400000)
        #barometerR.init()
        # ip робота, порт, ip компа, порт, mosi_pinid, miso_pinid, sck_pinid, eth_cs_pinid, eth_reset_pinid
        self.ethernetR = ethernet.EthernetW5500('192.168.0.177', 8080, "192.168.0.100", 8888, 19, 16, 18, 17, 20)
        self.ethernetR.get_mac_address()
        #servo_pins = [0,0,0,0,0,0,0,0] # заполнить
        #thruster = []
        #for pin in servo_pins:
        #    thruster.append(srv.Servo(pin,min_us=544.0,max_us=2400.0,min_deg=0.0,max_deg=180.0,freq=50))
        #self.gyroR = gyro.GyroscopeDataLogger()
        #manipulator = l298dcmotor.DCMotor()
        print("robot has initialized")
        
    def loop(self):
        print("Main loop started.")
        self.ethernetR.toSend = 'abcdef'
        #self.gyroR.set_zero_position()
        while(1):
            self.ethernetR.run()
            print(self.ethernetR.data)
            print(" ")
            #self.ethernetR.toSend = self.ethernetR.data # пример echo
            # host ip:port    192.168.0.100:8080
            #self.gyroR.read_gyroscope_data()
            
            
if __name__=="__main__":
    katran = robot()
    katran.loop()
    