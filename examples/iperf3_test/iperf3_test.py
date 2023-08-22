import machine
import network
import uiperf3

SERVER_IP= "192.168.11.100"

DEVICE_IP = "192.168.11.101"
GATEWAY = "192.168.11.1"
NETMASK = "255.255.255.0"
DNS = "8.8.8.8"

def wiznet_init():
    spi = machine.SPI(0, baudrate=2000000, mosi=machine.Pin(19), miso=machine.Pin(16), sck=machine.Pin(18))
    nic = network.WIZNET5K(spi, machine.Pin(17), machine.Pin(20))
    nic.active(True)
    nic.ifconfig((DEVICE_IP, NETMASK, GATEWAY, DNS))
    
    print('IP address :', nic.ifconfig())
    
def main():
    wiznet_init()
    uiperf3.client(SERVER_IP)
    
    
if __name__ == "__main__":
    main()
