# README.md

Based on [KiCad 9 Hardware Design Tutorial (TI MSPM0)](https://www.youtube.com/watch?v=O-zNn5k5Bn4) Youtube tutorial by Phil's Lab

## Microcontroller MSPM0G3507SPTR

Texas Instruments middle of the range MCU from MSP family:  80MHz Arm Cortex-M0+ MCU with 128KB flash 32KB SRAM 2x4Msps ADC, DAC, 3xCOMP, 2xOPA, CAN-FD, MATHA

(four UART, two I2C, two SPI, and CAN 2.0/FD)

https://www.ti.com/product/MSPM0G3507/part-details/MSPM0G3507SPTR

https://www.ti.com/lit/ds/symlink/mspm0g3507.pdf



## Project modified to add 9DOF

Two chips connected via I2C:

A 6DOF IMU: 

LSM6DSR - iNEMO inertial module: always-on 3D accelerometer and 3D gyroscope

LCSC# C784817

Datasheet: https://www.lcsc.com/datasheet/C784817.pdf

Arduino library: https://github.com/stm32duino/LSM6DSR



A 3-axis magnetic sensor 

MMC5983MA - 3-axis magnetic sensor with on-chip signal processing and integrated I2C/SPI bus 

LCSC# C404329

Datasheet: https://www.lcsc.com/datasheet/C404329.pdf

Add axes to silkscreen

Refer to:

https://www.memsic.com/magnetometer-5

PCB layout guidance

https://www.digikey.bg/en/pdf/m/memsic/magnetic-sensor-hardware-guideline

https://www.nxp.com/docs/en/application-note/AN4247.pdf

Arduino library: https://github.com/sparkfun/SparkFun_MMC5983MA_Magnetometer_Arduino_Library
