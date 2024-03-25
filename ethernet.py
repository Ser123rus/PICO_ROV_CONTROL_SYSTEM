from usocket import socket
import usocket
from machine import Pin, SPI
import machine
import network
import time

class EthernetW5500():
    def __init__(self, local_ip, local_port, remote_ip, remote_port, mosi_pinid, miso_pinid, sck_pinid, eth_cs_pinid, eth_reset_pinid):
        self.udp_socket = socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        self.udp_socket.bind((local_ip, local_port))
        self.udp_socket.settimeout(3)
        self.remote_addr = (remote_ip, remote_port)
        self.spi = SPI(0, 2_000_000, mosi=Pin(mosi_pinid), miso=Pin(miso_pinid), sck=Pin(sck_pinid))
        self.nic = network.WIZNET5K(self.spi, Pin(eth_cs_pinid), Pin(eth_reset_pinid))
        self.nic.active(True)
        self.data = None
        self.result = [91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 1, 1]
        self.toSend = '\x00\x00\x00\x00\x00\x00'
        self.nic.ifconfig((local_ip, '255.255.255.0', '192.168.1.1', '8.8.8.8'))
        
        while not self.nic.isconnected():
            time.sleep(5)
            print("Ethernet shield is not connected")
            
        print(self.nic.ifconfig())
        print("Ethernet configured")

    def get_mac_address(self):
        mac_address_bytes = machine.unique_id()
        mac_address_str = ':'.join(['{:02X}'.format(byte) for byte in mac_address_bytes])
        print("MAC Address:", mac_address_str)

    def receive(self):
        try:
            received_data, addr = self.udp_socket.recvfrom(8)
            print(f"Received data: {received_data} from {addr}")
            if self.data != received_data:
                print("Сохранение новых данных...")
                self.data = received_data
                for i in range(8):
                    self.result[i] = float(self.data[i])
        except Exception as e:
            print("Error receiving data:", e)
            self.result = [91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 1, 1]
            return

    def send(self, data):
        try:
            if data != None:
                self.udp_socket.sendto(data, self.remote_addr)
                print(f"Data sent: {data}")
        except Exception as e:
            print("Error sending data:", e)

    def run(self):
        self.send(self.toSend)
        self.receive()
        #await uasyncio.gather(self.send(self.toSend), self.receive()) # поменять отправляемое

if __name__ == "__main__":
    builtInLed = Pin(25, Pin.OUT)
    builtInLed.value(0)
    ethernet = EthernetW5500('192.168.0.177', 8080, '192.168.0.100', 8080, 19, 16, 18, 17, 20)
    ethernet.get_mac_address()
    while True:
        ethernet.run()