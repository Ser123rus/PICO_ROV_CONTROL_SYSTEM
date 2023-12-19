from usocket import socket
import usocket
from machine import Pin, SPI
import machine
import network
import time
import uasyncio

class EthernetW5500():
    def __init__(self, local_ip, local_port, remote_ip, remote_port, mosi_pinid, miso_pinid, sck_pinid, eth_cs_pinid, eth_reset_pinid):
        self.udp_socket = socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        self.udp_socket.bind((local_ip, local_port))
        self.remote_addr = (remote_ip, remote_port)
        self.spi = SPI(0, 2_000_000, mosi=Pin(mosi_pinid), miso=Pin(miso_pinid), sck=Pin(sck_pinid))
        self.nic = network.WIZNET5K(self.spi, Pin(eth_cs_pinid), Pin(eth_reset_pinid))
        self.nic.active(True)
        self.nic.ifconfig((local_ip, '255.255.255.0', '192.168.0.1', '8.8.8.8'))
        
        while not self.nic.isconnected():
            time.sleep(5)
            print("Ethernet shield is not connected")
            
        print(self.nic.ifconfig())
        print("Ethernet configured")

    def get_mac_address(self):
        mac_address_bytes = machine.unique_id()
        mac_address_str = ':'.join(['{:02X}'.format(byte) for byte in mac_address_bytes])
        print("MAC Address:", mac_address_str)

    async def receive(self):
        try:
            data, addr = self.udp_socket.recvfrom(8)
            print(f"Received data: {data.decode()} from {addr}")
            await uasyncio.sleep(1)
        except Exception as e:
            print("Error receiving data:", e)

    async def send(self, data):
        try:
            self.udp_socket.sendto(data, self.remote_addr)
            print(f"Data sent: {data}")
        except Exception as e:
            print("Error sending data:", e)

    async def run(self):
        await uasyncio.gather(self.receive(), self.send(b"Hello, World!"))

if __name__ == "__main__":
    builtInLed = Pin(25, Pin.OUT)
    builtInLed.value(0)
    ethernet = EthernetW5500('192.168.0.177', 8080, '192.168.0.100', 8080, 19, 16, 18, 17, 20)
    ethernet.get_mac_address()
    
    loop = uasyncio.get_event_loop()
    loop.create_task(ethernet.run())
    loop.run_forever()