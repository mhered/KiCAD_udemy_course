# README.md

Design of a Raspberry PICO IoT device on 4-layer PCB with sensors and more. Ref. https://www.youtube.com/watch?v=tCulctQqdhM by morten

Features:

* Raspberry Pi Pico (W)
* RS485 / MOD-bus interface
*  DIP-switch for MOD-bus address selection 
* SHT31-DIS high precision temperature and humidity sensor. I use P version (with protective film for reflow)
* QWIIC connector 
* Reset Button  
* User Button 
* User RGB LED 
* 2x5 pin SPI bus expansion header   
* Power relay (230V - 16A)      
* Wide range input voltage +8V to 24V DC 

For the mechanical side of things:

* 4-layer board design
* Size 80x80mm
* 4 x 3.2mm mounting holes 

## Notes on components

TRACO Power TSR-1 2450 - DC-DC step-down (buck) regulator (replaces 78xx linear regulators) with a single 5 V output at up to 1A



DC power jack

1A polyfuse to protect input - 1.1A hold current polyfuse > selected MF-R110 (TH) / MF-SM100-2 (SMT)

diode 24V tranzorb (used SMAJ24A)

3.3V bar: 

* Check out this [hardware design with RP2040](https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008279-DS-1-hardware-design-with-rp2040.pdf)  guide ([local copy](./assets/RP-008279-DS-1-hardware-design-with-rp2040.pdf))
* LDO for 3.3.V - TLV1117-33IDCYR 800mA Low-Dropout Linear Regulator, 3.3V fixed output, SOT-223-4

Pico:

* 1N5819 40V 1A Schottky Barrier Rectifier Diode, DO-41 to protect Vin. iaw ChatGPT a standard SMD analog is the **SS14** series — same **1 A / 40 V** rating in a **DO-214AC (SMA) package**

Relay:

* diode in reverse: LL4148 > replaced by SS14

Transceiver: THVD1406DR transceiver (made custom symbol) instead of MAX3485 but now I am not sure I am wiring it properly!

# Schematics

![](./assets/schematics_v1.0.png)
