import sys
import yaml
import RPi.GPIO as GPIO
import time
import datetime
import structlog
from pathlib import Path
import csv
import os
import glob
from daemon import Daemon
from bmp183 import bmp183
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import psycopg2

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# try:
#    import thread
# except ImportError:
#     import _thread as thread


class CSVWriter:

    def __init__(self, filename='test.csv', header=[]):
        newfile = False
        self._header = header
        outfile = Path(filename)
        if not outfile.is_file():
            # File doesn't exist, will be created, print header too
            newfile = True
        self.fn = open(filename, 'a')
        self._day = int(datetime.date.today().day)
        print("Date:" + str(self._day))
        self.csv = csv.writer(self.fn, delimiter=',')
        print("Size" + str(len(header)))
        if newfile:
            # new file so print header
            self.csv.writerow(self._header)

    def writedata(self, dataobj, day):
        if (self._day != day):
            dt = datetime.date.today()
            filename = "data-"+dt.strftime("%Y-%m-%d") + ".csv"
            self.fn.close()
            self = CSVWriter(filename, self._header)
            self.csv.writerow(self._header)
            self._day = int(datetime.date.today().day)
        self.csv.writerow(dataobj)

    def __del__(self):
        self.fn.close()


class StationConfig:
    """Configuration parser"""
    def __init__(self, file='config.yaml'):
        with open(file, 'r') as ymlfile:
            try:
                self.configs = yaml.load(ymlfile)
            except yaml.YAMLError as exc:
                sys.exit("Fatal: Config file cannot be parsed as correct YAML")


class WeatherDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(.05)


class WeatherData:

    def __init__(self, t=0, p=0):
        self._timestamp = datetime.datetime.utcnow()
        self._temp = t
        self._pressure = p
        self._humidityDHT = None
        self._temperatureDHT = None
        self._ds18b20temp = None
        self._light = 0
        self._winddir = 0
        self._windspeed = 0
        self._rain = 0
        self._air1 = 0
        self._air2 = 0
        self._soilmoisture = 0
        self._dataformatversion = 1
        self._DHTsuccess = 0

    @property
    def timeUTC(self):
        s = self._timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
        return s[:-3]

    @property
    def pressureMillibar(self):
        # Raw is Pascals, divide by 100 to get millibar
        """getting"""
        return "%0.1f" % ((self._pressure/100),)

    @property
    def pressureInchesHG(self):
        # Raw is Pascals, divide by 3389.39 you'll get inches-Hg.
        """getting"""
        return "%0.2f" % ((self._pressure/3389.39),)

    @property
    def air1(self):
        """getting"""
        return self._air1

    @air1.setter
    def air1(self, value):
        if value is not None and 0.0 <= value <= 1024.0:
            self._air1 = value
        else:
            self._air1 = 0.0

    @property
    def light(self):
        """getting"""
        return self._light

    @light.setter
    def light(self, value):
        if value is not None and 0.0 <= value <= 1024.0:
            self._light = value
        else:
            self._light = 0.0

    @property
    def winddir(self):
        """getting"""
        return self._winddir

    @winddir.setter
    def winddir(self, value):
        if value is not None and 0.0 <= value <= 1024.0:
            self._winddir = value
        else:
            self._winddir = 0.0

    @property
    def windspeed(self):
        """getting"""
        return self._windspeed

    @windspeed.setter
    def windspeed(self, value):
        if value is not None and 0.0 <= value <= 1024.0:
            self._windspeed = value
        else:
            self._windspeed = 0.0

    @property
    def rain(self):
        """getting"""
        return self._rain

    @rain.setter
    def rain(self, value):
        if value is not None and 0.0 <= value <= 1024.0:
            self._rain = value
        else:
            self._rain = 0.0

    @property
    def air2(self):
        """getting"""
        return self._air2

    @air2.setter
    def air2(self, value):
        if value is not None and 0.0 <= value <= 1024.0:
            self._air2 = value
        else:
            self._air2 = 0.0

    @property
    def soilmoisture(self):
        """getting"""
        return self._soilmoisture

    @soilmoisture.setter
    def soilmoisture(self, value):
        if value is not None and 0.0 <= value <= 1024.0:
            self._soilmoisture = value
        else:
            self._soilmoisture = 0.0

    @property
    def dataformatversion(self):
        """getting"""
        return self._dataformatversion

    @property
    def ds18b20temp(self):
        """getting"""
        return self._ds18b20temp

    @ds18b20temp.setter
    def ds18b20temp(self, value):
        if value is not None and -40.0 <= value <= 200.0:
            self._ds18b20temp = "%0.2f" % (value,)
        else:
            self._ds18b20temp = 0.0

    @property
    def humidityDHT(self):
        """getting"""
        return self._humidityDHT

    @property
    def temperatureDHT(self):
        """getting"""
        return self._temperatureDHT

    @humidityDHT.setter
    def humidityDHT(self, value):
        if value is not None and 0.0 <= value <= 100.0:
            self._humidityDHT = value
        else:
            self._humidityDHT = 0.0

    @temperatureDHT.setter
    def temperatureDHT(self, value):
        # Store in F, so convert from C:
        if value is not None and 0.0 <= value <= 200.0:
            self._temperatureDHT = "%0.2f" % ((value*1.8)+32,)
        else:
            self._temperatureDHT = 0.0

    @property
    def tempF(self):
        """getting"""
        return "%0.1f" % ((self._temp*1.8)+32,)

    @property
    def tempC(self):
        """getting"""
        return "%0.1f" % (self._temp,)

    def exportdata(self):
        return [self.timeUTC, self.tempF, self.pressureMillibar,
                      self.temperatureDHT, self.humidityDHT, self.light,
                      self.winddir, self.windspeed, self.rain,
                      self.ds18b20temp, self.soilmoisture, self.air1,
                      self.air2, self.dataformatversion]

    def day(self):
        s = self._timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
        return int(s[8:10])

    def describedata(self, v=None):
        v = v or self._dataformatversion
        if v == 1:
            return ["Timestamp UTC", "BMP Temp F", "BMP Pressure Millibar", 
                    "DHT Temp C", "DHT Humidity %", "Light Count", 
                    "Winddir ", "Windspeed Count", "Rain Count", "Soil Temp", 
                    "Soil Moisture", "Air Sensor 1", "Air Sensor 2", "Data Format Version"] 
        else:
            return [v]

    @staticmethod
    def ds18b20_read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    @staticmethod
    def ds18b20_read_temp():
        lines = WeatherData.ds18b20_read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.02)
            lines = WeatherData.ds18b20_read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f


if __name__ == '__main__':

    logger = structlog.get_logger()
    GPIO.setwarnings(False)

    logger.info("Loading Configs...")
    cfg = StationConfig('config.yaml')
    # cfg.dumpcfg()

    logger.info("Getting Data Ready:")
    # Get our CSV Writer ready, pass in the Data Header for 1st line
    # dataout = CSVWriter("data-"+datetime.date.today().strftime("%Y-%m-%d") +
    #                    ".csv", WeatherData().describedata())
    try:
        connect_str = "dbname='weatherstation' user='weatherstation' " + \
                  "host='127.0.0.1' password='weatherstation'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)

        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()

        # create a new table with a single column called "name"
        # cursor.execute("""CREATE TABLE tutorials (name char(40));""")

        # run a SELECT statement - no data in there, but we can try it
        # cursor.execute("""SELECT * from weatherdata""")
        # rows = cursor.fetchall()
        # print("fetch all: " + str(rows))
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

    # Sensors
    logger.info("Getting Sensors Ready:")
    # print(cfg.configs['bmp183']['pin-sck'])
    bmp = bmp183(cfg.configs['bmp183']['pin-sck'],
                 cfg.configs['bmp183']['pin-sdo'],
                 cfg.configs['bmp183']['pin-sdi'],
                 cfg.configs['bmp183']['pin-cs'])

    # mcp = Adafruit_MCP3008.MCP3008(clk=cfg.configs['mcp3008']['pin-clk'],
    #                               cs=cfg.configs['mcp3008']['pin-cs'],
    #                               miso=cfg.configs['mcp3008']['pin-miso'],
    #                               mosi=cfg.configs['mcp3008']['pin-mosi'])
    # Hardware SPI configuration:
    SPI_PORT = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    datalast = None
    while True:
        start = datetime.datetime.now()

        # print(sorted(list(data._dumprow)))
        bmp.measure_pressure()
        data = WeatherData(bmp.temperature, bmp.pressure)
        print("Temperature: " + data.tempF + " deg F")
        # print("Temperature: " + data.tempC + " deg C")
        print("Pressure : " + data.pressureMillibar + " millibar")
        # print("Pressure : " + data.pressureInchesHG + " inches-Hg")

        (tempc, data.ds18b20temp) = data.ds18b20_read_temp()
        print("1-wire temp: " + str(data.ds18b20temp))

        humidity, temperature = Adafruit_DHT.read(11, 5)
        if humidity is not None and temperature is not None:
            data.humidityDHT = humidity
            data.temperatureDHT = temperature 
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(
                temperature, humidity))
        else:
            # if datalast is not None:
            #    humidity = datalast.humidityDHT
            #    temperature = datalast.temperatureDHT
            print('Failed to get reading. Try again!')

        # Analog Readings
        values = [0]*8
        for i in range(8):
            # The read_adc function will get the value
            # of the specified channel (0-7).
            values[i] = mcp.read_adc(i)
        # Print the ADC values.
        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |\
 {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
        print('-' * 57)
        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |\
 {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
        
        data.air1 = values[cfg.configs['air1']['analog-ch']]
        data.air2 = values[cfg.configs['air2']['analog-ch']]
        data.light = values[cfg.configs['lightresistor']['analog-ch']]
        data.soilmoisture = values[cfg.configs['soilmoisture']['analog-ch']]

        # Output:
        print("Data:")
        print(list(data.exportdata()))
        sql = """INSERT into weatherdata (measurement, bmp_temp_f,
              bmp_pressuer_millibar, dht_temp_f, dht_humidity_perc,
              light_reading, wind_dir_value, wind_speed_count, rain_count,
              soil_temp, soil_humidity, air_1,  air_2, data_version) values
              (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"""
        insertdata = list(data.exportdata()) 

        try:
            cursor.execute(sql, insertdata)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # dataout.writedata(data.exportdata(), data.day())
        # print("Day: " + str(data.day()))
        # print ("Desc: ")
        # print(data.describedata())
        datalast = data
        # time.sleep(0.15)
        now = datetime.datetime.now()
        print("Start Sec: " + str(start.second) + " " + str(start.microsecond))
        print("Now   Sec: " + str(now.second) + " " + str(now.microsecond))

    exit(0)

    daemon = WeatherDaemon('/tmp/weatherdaemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logger.info("Starting up...")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            logger.info("Shutting down...")
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            logger.info("Restarting...")
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
            # sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)

    # Date Calcs
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    logger.debug("Tomorrow: " + str(tomorrow.month) + " " + str(tomorrow.day))
