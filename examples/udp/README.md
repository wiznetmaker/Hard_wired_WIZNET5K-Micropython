# UDP Multicast with MicroPython on WIZnet

In this tutorial, we'll cover how to set up a simple UDP multicast application using MicroPython on a WIZnet chip. Multicast is a powerful feature that allows a single sender to communicate with multiple recipients without knowing their specific addresses. This can be beneficial in various IoT scenarios where devices need to broadcast their status or discover other devices on the same network.

## Prerequisites:
- A device with a WIZnet chip.
- MicroPython firmware installed on the device.
- Basic knowledge of networking and Python programming.

## Step-by-Step Guide:

### 1. Setting up the Network:

Before we start multicasting data, we need to set up the network:

```python
DEVICE_IP = "192.168.11.104"
GATEWAY = "192.168.11.1"
NETMASK = "255.255.255.0"
DNS = "8.8.8.8"

def wiznet_init():
    try:
        spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
        nic = network.WIZNET5K(spi, Pin(17), Pin(20))
        nic.active(True)
        nic.ifconfig((DEVICE_IP, NETMASK, GATEWAY, DNS))
        print('IP address :', nic.ifconfig())
    except Exception as e:
        print("Error in wiznet_init:", e)
        raise 
```

In the code above, we initiate a SPI communication with the WIZnet chip and set the device's network configurations.

### 2. Preparing for Multicast:

Before sending or receiving multicast messages, our device must join a multicast group:
Here, we create a socket, bind it to the multicast IP and port, and then join the multicast group.

```python
def ip_to_bytes(ip_str):
    return bytes(map(int, ip_str.split('.')))

def udp_multicast_init(multicast_ip='224.0.10.1', port=50000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((multicast_ip, port))
    mreq = struct.pack('4sl', ip_to_bytes(multicast_ip))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return s
```

__* UDP Multicast Socket Initialization:__

1. **Socket Creation**: A new UDP socket is created using `socket.AF_INET` (IPv4) and `socket.SOCK_DGRAM` (UDP).
2. **Setting Socket Options**: 
    - The socket option `SO_REUSEADDR` is set to 1. 
    - This allows the OS to reuse the socket's address and port numbers.
    - Ensures multiple sockets can bind and listen on the same multicast address and port.
3. **Binding the Socket**: The socket is bound to the specified multicast IP address and port number.
4. **Pause for Binding Completion**: 
    - The code pauses for 1.5 seconds using `time.sleep(1.5)`.
    - This ensures that the bind operation completes without any issues. 
    - This delay might be unnecessary depending on the system.
5. **Joining a Multicast Group**:
    - To inform the OS that this socket wishes to join a multicast group, the `IP_ADD_MEMBERSHIP` option is set on it.
    - The required value for this option is a packed byte string representing the multicast address to join. 
    - This is achieved by passing the `multicast_ip` to the `ip_to_bytes` function and using `struct.pack` to format it.
6. **Ready for Communication**: With these steps, the socket becomes ready to receive data sent to the multicast group.



### 3. Running the Application:

Finally, in our main loop, we continuously receive multicast messages and then send them to ***another multicast group***:

```python
def main():    
    wiznet_init()
    sock = udp_multicast_init()
    while True:        
        message, addr = sock.recvfrom(1024)
        print(f"Received: {message} from {addr}")
        sock.sendto(message, ('224.0.10.2', 50000))
        print("Data sent.")
    
main()
```

## Conclusion:
This tutorial provides a basic introduction to setting up UDP multicast with MicroPython on a WIZnet chip. Multicast can be especially useful in IoT applications for broadcasting and discovering devices on the same network. You can further expand this example by adding more advanced features like error handling, message acknowledgment, and more. Happy coding!