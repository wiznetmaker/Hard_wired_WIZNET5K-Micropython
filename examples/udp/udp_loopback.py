import machine
import network
import socket
import time

DEVICE_IP = "192.168.11.101"
GATEWAY = "192.168.11.1"
NETMASK = "255.255.255.0"
DNS = "8.8.8.8"
SPI_BAUDRATE = 2000000
SPI_MOSI = 19
SPI_MISO = 16
SPI_SCK = 18
SPI_CS = 17
SPI_RST = 20

def wiznet_init():
    spi = machine.SPI(0, baudrate=SPI_BAUDRATE, mosi=machine.Pin(SPI_MOSI), miso=machine.Pin(SPI_MISO), sck=machine.Pin(SPI_SCK))
    nic = network.WIZNET5K(spi, machine.Pin(SPI_CS), machine.Pin(SPI_RST))
    nic.active(True)
    nic.ifconfig((DEVICE_IP, NETMASK, GATEWAY, DNS))
    
    print('IP address :', nic.ifconfig())
    
def main():
    wiznet_init()
    
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 5000))

    print("Loopback server Open!")
    while True:
        data, addr = s.recvfrom(1024)
        print("Received message:", data, "from:", addr)

        if data != 'NULL':
            s.sendto(data, addr)
            
if __name__ == "__main__":
    main()