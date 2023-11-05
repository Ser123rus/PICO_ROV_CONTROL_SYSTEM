from usocket import socket
import usocket
from machine import Pin,SPI
import machine
import network
import time
from array import *

class EthernetW5500(): # '192.168.0.177', 8080, 19, 16, 18, 17, 20
    def __init__(self, local_ip, local_port, mosi_pinid, miso_pinid, sck_pinid, eth_cs_pinid, eth_reset_pinid):
        self.udp_socket = socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        self.udp_socket.bind((local_ip, local_port))
        self.udp_host = socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        self.spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
        self.nic = network.WIZNET5K(self.spi,Pin(17),Pin(20)) #spi,cs,reset pin
        self.nic.active(True)
        self.nic.ifconfig((local_ip, '255.255.255.0', '192.168.0.1', '8.8.8.8'))
        while not self.nic.isconnected():
            time.sleep(5)
            print("Ethernet shield is not connected")
        print(self.nic.ifconfig())
        print("Ethernet configured")
 
    def get_mac_address(self):
        # Get the MAC address as a bytes object
        mac_address_bytes = machine.unique_id()
        # Convert the MAC address to a readable string
        mac_address_str = ':'.join(['{:02X}'.format(byte) for byte in mac_address_bytes])
        print("MAC Address:", mac_address_str)
     
    def receive(self):
        try:
            data, addr = self.udp_socket.recvfrom(8)
            print(f"Received data: {data.decode()} from {addr}")
            time.sleep(1)
            return data
        except Exception as e:
            print("Error receiving data:", e)
                
    def send(self, data):
        try:
            self.udp_host.sendto(data, ('192.168.0.100', 8080))
            print(f"Data sent: {data}")
            time.sleep(1)
        except Exception as e:
            print("Error sending data:", e)
                
        


if __name__ == "__main__":
    builtInLed = Pin(25, Pin.OUT)
    builtInLed.value(0)
    ethernet = EthernetW5500('192.168.0.177', 8080, 19, 16, 18, 17, 20)
    ethernet.get_mac_address()
    ethernet.test_sending()
    