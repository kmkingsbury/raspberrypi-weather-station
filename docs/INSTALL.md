# Install

Raspberry Pi 3 Model B v1.2
* Base Install Raspbian GNU/Linux 8 (jessie)
* raspi-config Configure: Turn on Camera, SSH, VNC, change default password.
* turn on SPI ( ls -l /dev/spi* shows 2 items)
* Setup Wifi.
* Update / Upgrade / reboot
* Install vim
sudo apt-get install vim

## Base Packages
```
sudo apt-get install python3 git
```
## Specifics

### DHT11
```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd
sudo python3 setup.py install
```

### Hih 4030
https://antoniolopes.info/blog/2013/03/05/working-with-analog-sensors-in-the-raspberry-pi/
http://www.picaxeforum.co.uk/showthread.php?14938-Hih-4030&p=133532&viewfull=1#post133532
http://bildr.org/2012/11/hih4030-arduino/


### bmp183
https://www.adafruit.com/product/1900

https://github.com/PrzemoF/bmp183
```
sudo apt-get install python3-rpi.gpio
sudo apt-get install python3-numpy
```
test-humidity.py uses the bmp183.py module to talk to the bmp183
Choose the right pins and set in bmp183.py  lines 74 - 77:
```               
self.SCK = 17  # GPIO for SCK, other name SCLK
self.SDO = 22  # GPIO for SDO, other name MISO
self.SDI = 23  # GPIO for SDI, other name MOSI
self.CS = 27  # GPIO for CS, other name CE
```

### Soil Temp
* Enable 1-wire in the raspi-config menu.
* Yellow Wire goes to GPIO 4 (pin 7)
```
sudo apt-get install python3-w1thermsensor
```
## MQ2
https://tutorials-raspberrypi.com/configure-and-read-out-the-raspberry-pi-gas-sensor-mq-x/

### GPS:
apt-get install gpsd gpsd-clients python-gps

MCP3008-I:
https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
cd Adafruit_Python_MCP3008


http://www.ohmslawcalculator.com/voltage-divider-calculator
Direction
(Degrees)
Resistance
(Ohms)
Voltage
(V=5v, R=10k)
0, 33k, 3.84v,2.533
22.5, 6.57k, 1.98v
45, 8.2k, 2.25v
67.5, 891, 0.41v
90, 1k, 0.45v
112.5, 688, 0.32v
135, 2.2k, 0.90v
157.5, 1.41k, 0.62v
180, 3.9k, 1.40v
202.5, 3.14k, 1.19v
225, 16k, 3.08v
247.5, 14.12k, 2.93v
270, 120k, 4.62v
292.5, 42.12k, 4.04v
315, 64.9k, 4.78v
337.5, 21.88k, 3.43v

N	0	 33k	 3.84v	2.533	0.331	785.23
NNE	22.5	 6.57k	 1.98v	2.864	-1.377	887.84
NE	45	 8.2k	 2.25v	1.487	-1.217	460.97
NEE	67.5	891	 0.41v	0.27	2.73	83.7
E	90	 1k	 0.45v	3	-2.788	930
ESE	112.5	688	 0.32v	0.212	0.383	65.72
SE	135	 2.2k	 0.90v	0.595	-0.187	184.45
SES	157.5	 1.41k	 0.62v	0.408	0.518	126.48
S	180	 3.9k	 1.40v	0.926	-0.137	287.06
SSW	202.5	 3.14k	 1.19v	0.789	1.242	244.59
SW	225	 16k	 3.08v	2.031	-0.099	629.61
SWW	247.5	 14.12k	 2.93v	1.932	1.114	598.92
W	270	 120k	 4.62v	3.046	-0.379	944.26
WNW	292.5	 42.12k	 4.04v	2.667	0.192	826.77
NW	315	 64.9k	 4.78v	2.859	-0.594	886.29
NWN	337.5	 21.88k	 3.43v	2.265	-2.265	702.15
