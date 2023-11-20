Micropython and WIZnet offer a variety of firmware, but there may be instances where your specific hardware environment isn't supported.
In such cases, this guide will show you how to create the firmware you need. 

![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/f9bd71c3-fa6c-42d0-b48f-cc1f31287908)


* This tutorial uses the W5300 micropython project I've worked on as an example.

Git repository: https://github.com/Wiznet/W5300-TOE-MicroPython


---
 
## 1. Download from Git

The official Git address for Micropython is as follows:
 > https://github.com/micropython/micropython/tree/master

Please use `git clone` to download, as there are submodules and other components that may not be included in the zip file!


## 2. Code Structure

Let's get a basic understanding of the structure!
![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/06af3d89-fb0e-4635-b509-b057129dc1e6)

_It is described in the main README._

The necessary parts for our purposes are the `ports`, `lib`, and `extmod` directories.


### - PORTS

You can select your device or MCU in this derectory.
Typically, it follows the structure `ports/{MCUname}/boards/{board name}.`
- Ex1 W5500-EVB-PICO: ports/rp2/boards/W5500_EVB_PICO

- Ex2 Stm Nucleo board: ports/stm32/boards/NUCLEO_Fxxx

If you want to modify or add to the operations of each MCU (GPIO, SPI, I2C, etc.), please make changes or additions to the code found in `ports/{MCUname}.`

It depends on the Make structure, if you're adding new files, they may need to be included in the `CMakeLists.txt.`

 For example, to integrate WIZnet W5300 Bus functionality into an STM NucleoFxx board, you would add an fmc.c file, and  included in the CMakeLists.txt.

- __Add fmc.c__
  
![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/837443a9-1f16-4a39-9764-043d57cad45f)

- __Included in the CMakeLists.txt__
  
![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/8e1e379c-b1ca-4bec-83b0-fae8a986a813)

![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/b58fe017-ebc5-43c9-b200-b269f1e422c4)


And typically, the main function for each program is found in the `main.c` file within this directory.

 If you're looking to implement initialization routines, this is the section that you would modify.

- __implement initialization routines in main.c__
  ![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/f0ee940e-c714-4498-8b19-40bfadcc7070)



### - LIB

Manages the SDK and libraries for MCUs and modules. This directory contains third-party, low-level C libraries and SDKs. Libraries that do not target any specific platform are generally chosen based on them being independent and efficient.

For MCU-related SDKs, most of the necessary code is already included, so there's generally no need for significant additions. 

If you need to add modules like Network, LCD, or Sensors, etc.. please manage the related libraries in this directory. 

In the case of `WIZnet`, the `ioLibrary` is already provided officially and is linked in the Lib directory. `lib/wiznet5k`

![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/4d655d80-166a-44f6-bf3c-3687f27a62fb)



### - EXTMOD

additional (non-core) modules implemented in C. Think of it as a section where operations performed by micropython commands are implemented in C. 

The structure can be seen as `[Micropython: Commands]`– `[extmod: Command Handling]` – `[lib: Module Operation]` 

- Ex. network_wiznet5k.c: SPI to Bus(FMC)

I will demonstrate how to modify the extmod portion of the code as used in a micropython example. 
```python
Import network

self.nic = network.WIZNET5K(...)
self.nic.active(True)
```
Generally, for each micropython command, there is a corresponding function in the code. If you need to make changes to a specific command, concentrate on adjusting the related function.

Micropython `network.WIZNET5K(...)` = in network_wiznet5k.c `mp_obj_t wiznet5k_make_new(… )`
![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/5ee1a552-5817-4b9e-bbc1-fc49429240f9)

Micropython `self.nic.active(...)` = in network_wiznet5k.c `wiznet5k_active( … )`
![image](https://github.com/wiznetmaker/Hard_wired_WIZNET5K-Micropython/assets/107094499/98d5f177-32ab-4589-9288-f1c1d02e2c52)



---

This posting is based on the W5K series network, but with proper application, it can also be beneficial for your other modules.
