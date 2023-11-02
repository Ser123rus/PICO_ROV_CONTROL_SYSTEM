import network
from machine import Pin, SPI
import time
import socket
from servo import Servo
import uasyncio as asyncio
from array import *

local_ip = '192.168.0.177'
local_port = 8080

# Создаем объекты для управления сервоприводами
servo1 = Servo(Pin(2))
servo2 = Servo(Pin(3))
servo3 = Servo(Pin(4))
servo4 = Servo(Pin(5))
servo5 = Servo(Pin(6))
servo6 - Servo(Pin(7))
 
def w5500_init():
    spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    nic = network.WIZNET5K(spi, Pin(17), Pin(20)) # spi, cs, reset pin
    nic.active(True)
    nic.ifconfig((local_ip, '255.255.255.0', '192.168.0.1', '8.8.8.8'))
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
    print(nic.ifconfig())


async def receive_udp_packets():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((local_ip, local_port))

    while True:
        data, addr = await udp_socket.recvfrom(6)
        print(f"Received data: {data.decode()} from {addr}")

        # Распределение данных на сервоприводы
        servo1_position = int(data[0])
        servo2_position = int(data[1])
        servo3_position = int(data[2])
        servo4_position = int(data[3])
        servo5_position = int(data[4])
        servo6_position = int(data[5])
        
        # Установка позиций сервоприводов
        servo1.angle(servo1_position)
        servo2.angle(servo2_position)
        servo3.angle(servo3_position)
        servo4.angle(servo4_position)
        servo5.angle(servo5_position)
        servo6.angle(servo6_position)

        await asyncio.sleep(1)


def main():
    w5500_init()

    loop = asyncio.get_event_loop()
    loop.create_task(receive_udp_packets())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

if __name__ == "__main__":
    main()