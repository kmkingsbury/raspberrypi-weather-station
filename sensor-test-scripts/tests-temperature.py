# http://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
# sudo pip3 install w1thermsensor
# Raspi-conf add in 1-wire enable

# Black gnd
# Red resistor & 3v3
# Yellow resistor & #4

#
import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

def CtoF( celsius ):
    return celsius * 9/5 + 32


while True:
    temperature = sensor.get_temperature()
    print("The temperature is %s F" % CtoF(temperature))
    time.sleep(1)
