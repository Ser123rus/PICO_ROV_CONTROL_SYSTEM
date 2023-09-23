from usocket import socket
import usocket
from machine import Pin,SPI
import machine
import network
import time
from array import *

builtInLed = Pin(25, Pin.OUT)
local_ip = '192.168.0.177'
local_port = 8080
udp_socket = socket(usocket.AF_INET, usocket.SOCK_DGRAM)
udp_socket.bind((local_ip, local_port))

def w5500_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    nic.ifconfig((local_ip, '255.255.255.0', '192.168.0.1', '8.8.8.8'))
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
    print(nic.ifconfig())
 
 
def get_mac_address():
    # Get the MAC address as a bytes object
    mac_address_bytes = machine.unique_id()

    # Convert the MAC address to a readable string
    mac_address_str = ':'.join(['{:02X}'.format(byte) for byte in mac_address_bytes])

    print("MAC Address:", mac_address_str)
 
 
def test_sending():
    
    while(1):
        try:
            builtInLed.value(1)
            data, addr = udp_socket.recvfrom(8)
            print(f"Received data: {data.decode()} from {addr}")
            time.sleep(1)
        except Exception as e:
            print("Error receiving data:", e)
    

if __name__ == "__main__":
    builtInLed.value(0)
    w5500_init()
    get_mac_address()
    test_sending()
    