from bmp183 import bmp183
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

bmp = bmp183()
bmp.measure_pressure()
print ("Temperature: ", (bmp.temperature*1.8)+32, "deg F")
print ("Pressure: ", bmp.pressure / 100.0, " hPa")
quit()
