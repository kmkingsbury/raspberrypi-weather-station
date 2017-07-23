import RPi.GPIO as GPIO
import time
import numpy

def __del__(self):
    if Groupclass:
        Groupclass.count -= 1

class bmp183():
        'Class for Bosch BMP183 pressure and temperature sensor with SPI interface as sold by Adafruit'
        # BMP183 registers
        BMP183_REG = {
            #@ Calibration data
            'CAL_AC1': 0xAA,
            'CAL_AC2': 0xAC,
            'CAL_AC3': 0xAE,
            'CAL_AC4': 0xB0,
            'CAL_AC5': 0xB2,
            'CAL_AC6': 0xB4,
            'CAL_B1': 0xB6,
            'CAL_B2': 0xB8,
            'CAL_MB': 0xBA,
            'CAL_MC': 0xBC,
            'CAL_MD': 0xBE,

            #@ Chip ID. Value fixed to 0x55. Useful to check if communication works
            'ID': 0xD0,
            'ID_VALUE': 0x55,

            #@ VER Undocumented
            'VER': 0xD1,

            #@ SOFT_RESET Write only. If set to 0xB6, will perform the same sequence as power on reset.
            'SOFT_RESET': 0xE0,

            #@ CTRL_MEAS Controls measurements
            'CTRL_MEAS': 0xF4,

            #@ DATA
            'DATA': 0xF6,
        }

        # BMP183 commands
        BMP183_CMD = {
            #@ Chip ID Value fixed to 0x55. Useful to check if communication works
            'ID_VALUE': 0x55,

            # SPI bit to indicate READ or WRITE operation
            'READWRITE': 0x80,

            # Read TEMPERATURE, Wait time 4.5 ms
            'TEMP': 0x2E,
            'TEMP_WAIT': 0.0045,

            # Read PRESSURE
            'PRESS': 0x34,  # 001

            # PRESSURE reading modes
            # Example usage: (PRESS || (OVERSAMPLE_2 << 4)
            'OVERSAMPLE_0': 0x0,  # ultra low power, no oversampling, wait time 4.5 ms
            'OVERSAMPLE_0_WAIT': 0.0045,
            'OVERSAMPLE_1': 0x1,  # standard, 2 internal samples, wait time 7.5 ms
            'OVERSAMPLE_1_WAIT': 0.0075,
            'OVERSAMPLE_2': 0x2,  # high resolution, 4 internal samples, wait time 13.5 ms
            'OVERSAMPLE_2_WAIT': 0.0135,
            'OVERSAMPLE_3': 0x3,  # ultra high resolution, 8 internal samples, Wait time 25.5 ms
            'OVERSAMPLE_3_WAIT': 0.0255,
        }

        def __init__(self):
                self.temperature = 0
                self.pressure = 0
                # Setup Raspberry PINS, as numbered on BOARD
                self.SCK = 11  # GPIO for SCK, other name SCLK
                self.SDO = 15  # GPIO for SDO, other name MISO
                self.SDI = 16  # GPIO for SDI, other name MOSI
                self.CS = 13  # GPIO for CS, other name CE

                # SCK frequency 1 MHz
                self.delay = 1 / 1000000.0
                self.set_up_gpio()

                # Check comunication / read ID
                ret = self.read_byte(self.BMP183_REG['ID'])
                if ret != self.BMP183_CMD['ID_VALUE']:
                        print ("BMP183 returned ", ret, " instead of 0x55. Communication failed, expect problems.")

                self.read_calibration_data()
                # Proceed with initial pressure/temperature measurement
                self.measure_pressure()

        def __del__(self):
                self.cleanup_gpio()

        def set_up_gpio(self):
                # GPIO initialisation
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.SCK, GPIO.OUT, initial=GPIO.HIGH)
                GPIO.setup(self.CS, GPIO.OUT, initial=GPIO.HIGH)
                GPIO.setup(self.SDI, GPIO.OUT)
                GPIO.setup(self.SDO, GPIO.IN)

        def cleanup_gpio(self):
                # GPIO clean up
                GPIO.cleanup(self.SCK)
                GPIO.cleanup(self.CS)
                GPIO.cleanup(self.SDI)
                GPIO.cleanup(self.SDO)

        def read_byte(self, addr):
                # Read byte from SPI interface from address "addr"
                ret_value = self.spi_transfer(addr, 0, 1, 8)
                return ret_value

        def read_word(self, addr, extra_bits=0):
                # Read word from SPI interface from address "addr", option to extend read by up to 3 bits
                ret_value = self.spi_transfer(addr, 0, 1, 16 + extra_bits)
                return ret_value

        def write_byte(self, addr, value):
                # Write byte of "value" to SPI interface at address "addr"
                self.spi_transfer(addr, value, 0, 8)

        def spi_transfer(self, addr, value, rw, length):
                # Bit banging at address "addr", "rw" indicates READ (1) or WRITE (1) operation
                ret_value = 0
                if (rw == 0):
                        spi_addr = addr & (~self.BMP183_CMD['READWRITE'])
                else:
                        spi_addr = addr | self.BMP183_CMD['READWRITE']

                GPIO.output(self.CS, 0)
                time.sleep(self.delay)
                for i in range(8):
                        bit = spi_addr & (0x01 << (7 - i))
                        if (bit):
                                GPIO.output(self.SDI, 1)
                        else:
                                GPIO.output(self.SDI, 0)
                        GPIO.output(self.SCK, 0)
                        time.sleep(self.delay)
                        GPIO.output(self.SCK, 1)
                        time.sleep(self.delay)

                if (rw == 1):
                        for i in range(length):
                                GPIO.output(self.SCK, 0)
                                time.sleep(self.delay)
                                bit = GPIO.input(self.SDO)
                                GPIO.output(self.SCK, 1)
                                ret_value = (ret_value << 1) | bit
                                time.sleep(self.delay)

                if (rw == 0):
                        for i in range(length):
                                bit = value & (0x01 << (length - 1 - i))
                                if (bit):
                                        GPIO.output(self.SDI, 1)
                                else:
                                        GPIO.output(self.SDI, 0)
                                GPIO.output(self.SCK, 0)
                                time.sleep(self.delay)
                                GPIO.output(self.SCK, 1)
                                time.sleep(self.delay)
                GPIO.output(self.CS, 1)
                return ret_value

        def read_calibration_data(self):
                # Read calibration data
                self.AC1 = numpy.int16(self.read_word(self.BMP183_REG['CAL_AC1']))
                self.AC2 = numpy.int16(self.read_word(self.BMP183_REG['CAL_AC2']))
                self.AC3 = numpy.int16(self.read_word(self.BMP183_REG['CAL_AC3']))
                self.AC4 = numpy.uint16(self.read_word(self.BMP183_REG['CAL_AC4']))
                self.AC5 = numpy.uint16(self.read_word(self.BMP183_REG['CAL_AC5']))
                self.AC6 = numpy.uint16(self.read_word(self.BMP183_REG['CAL_AC6']))
                self.B1 = numpy.int16(self.read_word(self.BMP183_REG['CAL_B1']))
                self.B2 = numpy.int16(self.read_word(self.BMP183_REG['CAL_B2']))
                self.MB = numpy.int16(self.read_word(self.BMP183_REG['CAL_MB']))
                self.MC = numpy.int16(self.read_word(self.BMP183_REG['CAL_MC']))
                self.MD = numpy.int16(self.read_word(self.BMP183_REG['CAL_MD']))

        def measure_temperature(self):
                # Start temperature measurement
                self.write_byte(self.BMP183_REG['CTRL_MEAS'], self.BMP183_CMD['TEMP'])
                # Wait
                time.sleep(self.BMP183_CMD['TEMP_WAIT'])
                # Read uncmpensated temperature
                self.UT = numpy.int32(self.read_word(self.BMP183_REG['DATA']))
                self.calculate_temperature()

        def measure_pressure(self):
                # Measure temperature - required for calculations
                self.measure_temperature()
                # Read 3 samples of uncompensated pressure
                UP = {}
                for i in range(3):
                        # Start pressure measurement
                        self.write_byte(self.BMP183_REG['CTRL_MEAS'], self.BMP183_CMD['PRESS'] | (self.BMP183_CMD['OVERSAMPLE_3'] << 4))
                        # Wait for conversion
                        time.sleep(self.BMP183_CMD['OVERSAMPLE_3_WAIT'])
                        # Store uncmpensated pressure for averaging
                        UP[i] = numpy.int32(self.read_word(self.BMP183_REG['DATA'], 3))

                self.UP = (UP[0] + UP[1] + UP[2]) / 3
                self.calculate_pressure()

        def calculate_pressure(self):
                # Calculate atmospheric pressure in [Pa]
                self.B6 = self.B5 - 4000
                X1 = (self.B2 * (self.B6 * self.B6 / 2 ** 12)) / 2 ** 11
                X2 = self.AC2 * self.B6 / 2 ** 11
                X3 = X1 + X2
                self.B3 = (((numpy.uint32(self.AC1 * 4 + X3)) << self.BMP183_CMD['OVERSAMPLE_3']) + 2) / 4
                X1 = self.AC3 * self.B6 / 2 ** 13
                X2 = (self.B1 * (self.B6 * self.B6 / 2 ** 12)) / 2 ** 16
                X3 = ((X1 + X2) + 2) / 2 ** 2
                self.B4 = numpy.uint32(self.AC4 * (X3 + 32768) / 2 ** 15)
                self.B7 = (numpy.uint32(self.UP) - self.B3) * (50000 >> self.BMP183_CMD['OVERSAMPLE_3'])
                p = numpy.uint32((self.B7 * 2) / self.B4)
                X1 = (p / 2 ** 8) * (p / 2 ** 8)
                X1 = int(X1 * 3038) / 2 ** 16
                X2 = int(-7357 * p) / 2 ** 16
                self.pressure = p + (X1 + X2 + 3791) / 2 ** 4

        def calculate_temperature(self):
                #Calculate temperature in [degC]
                X1 = (self.UT - self.AC6) * self.AC5 / 2 ** 15
                X2 = self.MC * 2 ** 11 / (X1 + self.MD)
                self.B5 = X1 + X2
                self.T = (self.B5 + 8) / 2 ** 4
                self.temperature = self.T / 10.0
