import time
from machine import Pin, PWM, SPI
import usocket

servos = [] #servo obj
servo_pins = [15, 14, 13, 12, 11, 10] #Servo Pins
for i in servo_pins:
    pwm = machine.PWM(machine.Pin(i))
    pwm.freq(50)
    servo = machine.PWM(machine.Pin(i), freq=50, duty=0)
    servos.append(servo)

def angle_to_pulse(angle):
    # angels in servo impulse
    return int((angle / 180) * (2400 - 544) + 544)

#sock init
socket_open = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)

# связываем сокет с адресом и портом
ip_address = "192.168.0.10" # IP Pico
port = 8888 #Port
socket_open.bind((ip_address, port))

computer_address = ("192.168.0.1", 9999) #PC adrr

while True:
    #thruster init
    angles = [180, 180, 180, 180, 180, 180]
    for i in range(len(servos)):
        servos[i].duty_u16(angle_to_pulse(angles[i]))
    time.sleep_ms(2)
    
    angles = [90, 90, 90, 90, 90, 90]
    for i in range(len(servos)):
        servos[i].duty_u16(angle_to_pulse(angles[i]))
    time.sleep_ms(1.5)
    
    
    data, addr = socket_open.recvfrom(1024) #packet receive
    new_angles = data.decode().split(",") #call func ang -> servo_pulse
    for i in range(len(servos)):
        servos[i].duty_u16(angle_to_pulse(int(new_angles[i])))
