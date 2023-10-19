from machine import SPI, Pin
import socket
import struct
import machine
import network
import time


DEVICE_IP = "192.168.11.104"
GATEWAY = "192.168.11.1"
NETMASK = "255.255.255.0"
DNS = "8.8.8.8"

def wiznet_init():
    try:
        spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
        nic = network.WIZNET5K(spi,Pin(17),Pin(20))
    
        nic.active(True)
        nic.ifconfig((DEVICE_IP, NETMASK, GATEWAY, DNS))
    
        print('IP address :', nic.ifconfig())
    
    except Exception as e:
        print("Error in wiznet_init:", e)
        raise    

#instead of 'inet_aton'
def ip_to_bytes(ip_str):
    return bytes(map(int, ip_str.split('.')))

def udp_multicast_init(multicast_ip='224.0.10.1', port=50000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     
    s.bind((multicast_ip, 50000))
    time.sleep(1.5)
    
    mreq = struct.pack('4sl', ip_to_bytes(multicast_ip))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    return s

def main():
    
    wiznet_init()
    sock= udp_multicast_init()
 
    while True:        
        message, addr = sock.recvfrom(1024)
        print(f"Received: {message} from {addr}")
        
        #Send to another multicast group        
        sock.sendto(message, ('224.0.10.2', 50000))
        print("Data sent.")
    
main()