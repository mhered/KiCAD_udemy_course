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

THVD1406DR transceiver (made custom symbol)

DC power jack

1A polyfuse to protect input - 1.1A hold current polyfuse > selected MF-R110 (TH) / MF-SM100-2 (SMT)

diode 24V tranzorb (used SMAJ24A)

