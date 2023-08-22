# Ethernet Hat's LWIP vs Hard Wired Speed Comparison

In this project, we will explain how to create libraries for the LWIP and Hard-wired mode settings of the W5100S-EVB-Pico and W5500-EVB-Pico. We will also compare the network speeds of both modes using iperf3.

## Set up Linux
From the Linux desktop, open a terminal by doing Right click, then “Open a terminal here”. Then enter the following commands, one by one, to install the required software.

```cpp
  sudo apt-get install git
  sudo apt-get install make
  sudo apt-get install gcc
  sudo apt-get install gcc-arm-none-eabi

```
Enter your password when prompted. Press the “y” (or “o” if the language is french) key to accept the installation when prompted. Once the pre-requisite software is installed, it is necessary to retrieve the MicroPython project from the Git tool by writing to a terminal the following commands (open from a folder where the MicroPython utility will be placed)

## Download Code
The MicroPython cross-compiler must be built first, which will be used to pre-compile (freeze) built-in Python code. This cross-compiler is built and run on the host machine using:

```cpp
/* Clone */
git clone https://github.com/micropython/micropython.git

```

## Compile
The MicroPython cross-compiler must be built first, which will be used to pre-compile (freeze) built-in Python code. This cross-compiler is built and run on the host machine using:

```cpp
$ cd micropython
$ make -C mpy-cross
```

This command should be executed from the root directory of this repository. All other commands below should be executed from the `ports/rp2/` directory.

Building of the RP2 firmware is done entirely using CMake, although a simple Makefile is also provided as a convenience. To build the firmware run (from this directory):

```cpp
$cd ports/rp2
$ make BOARD={your-board-model} submodules
$ make BOARD={your-board-model} clean
$ make BOARD={your-board-model}
```

It is necessary to replace {your-board-model} with the name of the board that is being used.

For example, if you are using a `W5100S-EVB-Pico`, you will need to write the command:
```cpp
$ make BOARD=W5100S_EVB_PICO submodules
$ make BOARD=W5100S_EVB_PICO clean
$ make BOARD=W5100S_EVB_PICO
```
Or using a `W5500-EVB-Pico`, you will need to write the command:
```cpp
$ make BOARD=W5500_EVB_PICO submodules
$ make BOARD=W5500_EVB_PICO clean
$ make BOARD=W5500_EVB_PICO
```

The previous commands have generated a folder called build-{your– board–model} available in `/micropython/ports/rp2/{your-board-model}`
* The build folder is located in theyou opened the terminal.

Firmware can be deployed to the device by putting it into bootloader mode (hold down BOOTSEL while powering on or resetting) and then copying `firmware.uf2` to the USB mass storage device that appears.

# Setting up HardWired mode

The use of lwIP can be enabled or disabled by selecting the appropriate option in the configure `mpconfigboard.cmake` file located in the `ports/rp2/{your-board-model}`
```cpp
set(MICROPY_PY_LWIP 0)
```

>1: LWIP
>
>0: Hard wired

It is necessary to verify if the LWIP settings have been applied correctly. Add logs to the WIZNET5K initialization to check.

__LWIP__

```cpp
// line 173
#if WIZNET5K_WITH_LWIP_STACK
 ...
// line 210
STATIC void wiznet5k_init(void) {
 ...
	printf("\r\n ----WIZNET5K_WITH_LWIP_STACK----\r\n");
 ...
}

```

__Hard Wired__
```cpp
// line 351
#if WIZNET5K_PROVIDED_STACK
 ...
// line 370
STATIC void wiznet5k_init(void) {
 ...
	printf("\r\n ----WIZNET5K_PROVIDED_STACK----\r\n");
 ...    
}

```

And then, run the make command again to apply the updated settings and compile


## Performance tests with iperf3
The following serial terminal program is required for uIPerf3 test, download and install from below links.

&#10004;[**Thonny**][link-thonny]
&#10004;[**iPerf3**][link-iperf3]

First, run the iperf 3 server. Open a command prompt and enter the following command.
> iperf3.exe -s

![][link-iperf3_server]

Afterwards, run the iPerf3 Client from the your board.
Please use the attached `iperf3_test.py` file in `iperf3_test` folder.
>https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/examples/iperf3_test

Modify *the network information* and the *server IP* where iperf3.exe is running.

```cpp
SERVER_IP= "192.168.11.100"

DEVICE_IP = "192.168.11.101"
GATEWAY = "192.168.11.1"
NETMASK = "255.255.255.0"
DNS = "8.8.8.8"
```

Now let's run the iperf3 on your board.
*I use the Thonny IDE. If you have a preferred program, feel free to use it.

![][link-iperf3_clinet]

it was found that the bitrate of the device in __hard-wired mode is 80% higher__ than the LwIP.
>LWIP: 747 kbits/sec
>
>Hardwired: 1.34Mbits/sec

Therefore, to enhance the default network speed and performance for users,
I suggest to set the default mode to 'LwIP 0'.
This change will be applied unless the user requires specific customizations for their networking configurations.

<!--
Link
-->

[link-thonny]: https://thonny.org/
[link-iperf3]: https://iperf.fr/iperf-download.php

[link-iperf3_server]: https://github.com/Wiznet/W5300-TOE-MicroPython/blob/main/static/images/uiPerf3/iperf3_server.png
[link-iperf3_clinet]: https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/blob/main/images/iperf3_client.png
