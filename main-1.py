import barometer, ethernet, srv, gyro, l298dcmotor
from array import *

class robot():
    def __init__(self):
        #barometerR = barometer.MS5837_30BA(bus=1, scl_pinid=15, sda_pinid=14, i2c_freq=400000)
        #barometerR.init()
        self.ethernetR = ethernet.EthernetW5500('192.168.0.177', 8080, 19, 16, 18, 17, 20)
        self.ethernetR.get_mac_address()
        #servo_pins = [0,0,0,0,0,0,0,0] # заполнить
        #thruster = []
        #for pin in servo_pins:
        #    thruster.append(srv.Servo(pin,min_us=544.0,max_us=2400.0,min_deg=0.0,max_deg=180.0,freq=50))
        #gyroR = gyro.Gyro()
        #gyroR.start()
        #manipulator = l298dcmotor.DCMotor()
        print("robot has initialized")
        
    def loop(self):
        print("Main loop started.")
        while(1):
            # host ip:port    192.168.0.100:8080
            telemetryStub = array('b', [45, 91, 127, 1])
            self.ethernetR.send(telemetryStub)
            self.ethernetR.receive()
        

if __name__=="__main__":
    katran = robot()
    katran.loop()
    