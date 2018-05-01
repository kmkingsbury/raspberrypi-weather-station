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
# from RPi_AS3935 import RPi_AS3935  # for lightning, not working

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def windEventHandler(pin):
    # print("handling wind speed event")
    data.windspeed += 1


def rainEventHandler(pin):
    # print("handling rain event")
    global lastrainevent
    now = datetime.datetime.now()
    diff = (now-lastrainevent).total_seconds()
    if (diff > 0.25):
        data.rain += 1
    lastrainevent = datetime.datetime.now()


def handle_interrupt(channel):
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        print("Noise level too high - adjusting")
        sensor.raise_noise_floor()
    elif reason == 0x04:
        print("Disturber detected - masking")
        sensor.set_mask_disturber(True)
    elif reason == 0x08:
        now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
        distance = sensor.get_distance()
        print("We sensed lightning!")
        print("It was " + str(distance) + "km away. (%s)" % now)
        print("")


class CSVWriter:

    def __init__(self, filename='test.csv', header=[]):
        print("CSV init")
        newfile = False
        self._header = header
        self._fileday = None
        self._filename = filename
        outfile = Path(filename)
        if not outfile.is_file():
            # File doesn't exist, will be created, print header too
            print("CSV init file not exist")
            newfile = True
        self.fn = open(filename, 'a')
        self.fileday = int(datetime.datetime.utcnow().day)
        # print("CSV Date:" + str(self._day))
        self.csv = csv.writer(self.fn, delimiter=',')
        # print("Size" + str(len(header)))
        if newfile:
            # new file so print header
            print("CSV init print header")
            self.csv.writerow(self._header)

    def writedata(self, dataobj):
        print("CSV write")
        day = int(dataobj[0][8:10])  # parse string of 1st arrat item
        if (int(self.fileday) != int(day)):

            print("CSV not equal ")
            # usually at 11:59 so UTCnow will get next day.
            dt = datetime.datetime.utcnow()
            filename = "data-"+dt.strftime("%Y-%m-%d") + ".csv"
            print("Newfile: " + filename)
            print("Self Day vs Arg Day:" + str(self.fileday) + "-" + str(day))
            self.fn.close()
            print("CSV after close")
            self = CSVWriter(filename, self._header)
            print("CSV new self")
            self.fileday = int(day)
            # self.csv.writerow(self._header)
            # self.fileday = int(datetime.datetime.utcnow().day)
            # self._day = int(datetime.datetime.utcnow().day)
        print("CSV writerow")
        self.csv.writerow(dataobj)

        print("After:" + str(self.fileday))
        self.fn.flush()
        # print("csv write")
        return self

    def __del__(self):
        print("CSV Del")
        self.fn.close()

    @property
    def fileday(self):
        # Day of Month for rotating CSV file
        """getting"""
        print("Fileday get")
        return int(self._fileday)

    @fileday.setter
    def fileday(self, value):
        print("Fileday setter: "+str(value))
        if int(value) is not None and 0 <= int(value) <= 31:
            self._fileday = int(value)
        else:
            self._fileday = None


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
            time.sleep(.001)


class WeatherData:

    def __init__(self):
        self._timestamp = datetime.datetime.utcnow()
        self._tdelta = 0.00
        self._temp = 0
        self._pressure = 0
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
    def pressure(self):
        # Raw is Pascals
        """getting"""
        return "%0.2f" % (self._pressure)

    @pressure.setter
    def pressure(self, value):
        if value is not None and 0.0 <= value <= 100000.0:
            self._pressure = value
        else:
            self._pressure = 0.0

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
    def windspeed(self):
        """getting"""
        return self._windspeed

    @windspeed.setter
    def windspeed(self, throwaway):
        self._windspeed += 1

    @property
    def rain(self):
        """getting"""
        return self._rain

    @rain.setter
    def rain(self, throwaway):
        self._rain += 1

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
    def temp(self):
        """getting"""
        return "%0.1f" % (self._temp)

    @property
    def tempF(self):
        """getting"""
        return "%0.1f" % ((self._temp*1.8)+32,)

    @property
    def tempC(self):
        """getting"""
        return "%0.1f" % (self._temp)

    @temp.setter
    def temp(self, value):
        # Store in F, so convert from C:
        if value is not None and 0.0 <= value <= 200.0:
            self._temp = value
        else:
            self._temp = 0.0

    @property
    def tdelta(self):
        """getting"""
        return "%0.2f" % (self._tdelta)

    @tdelta.setter
    def tdelta(self, value):
        # Store in F, so convert from C:
        if value is not None and 0.00 <= value <= 200.00:
            self._tdelta = value
        else:
            self._tdelta = 0.00

    def exportdata(self):
        return [self.timeUTC, self.tdelta, self.tempF, self.pressureMillibar,
                self.temperatureDHT, self.humidityDHT, self.light,
                self.winddir, self.getwinddir(self.winddir), self.windspeed,
                self.rain, self.ds18b20temp, self.soilmoisture, self.air1,
                self.air2, self.dataformatversion]

    def day(self):
        s = self._timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
        return int(s[8:10])

    def describedata(self, v=None):
        v = v or self._dataformatversion
        if v == 1:
            return ["Timestamp UTC", "Timedelta sec", "BMP Temp F",
                    "BMP Pressure Millibar", "DHT Temp C", "DHT Humidity %",
                    "Light Count", "Winddir ", "Winddir Lookup",
                    "Windspeed Count", "Rain Count", "Soil Temp",
                    "Soil Moisture", "Air Sensor 1", "Air Sensor 2",
                    "Data Format Version"]
        else:
            return [v]

    def getwinddir(self, windreading):
        winddirtable = {
                        (867, 917): 'W',
                        (816, 866): 'NW',
                        (770, 815): 'WNW',
                        (714, 769): 'N',
                        (644, 713): 'NWN',
                        (598, 643): 'SW',
                        (521, 597): 'SWW',
                        (431, 520): 'NE',
                        (348, 430): 'NNE',
                        (269, 347): 'S',
                        (218, 268): 'SSW',
                        (159, 217): 'SE',
                        (112, 158): 'SES',
                        (90, 112): 'E',
                        (76, 89): 'NEE',
                        (33, 75): 'ESE'
                        }
        for key in winddirtable:
            if key[0] < windreading < key[1]:
                return winddirtable[key]

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
            time.sleep(0.001)
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
    dataout = CSVWriter("data-" +
                        datetime.datetime.utcnow().strftime("%Y-%m-%d") +
                        ".csv", WeatherData().describedata())
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

    # sensor = RPi_AS3935(address=0x00, bus=1)

    # sensor.set_indoors(True)
    # sensor.set_noise_floor(0)
    # sensor.calibrate(tun_cap=0x0F)

    data = WeatherData()
    lastrainevent = datetime.datetime.now()
    GPIO.setup(cfg.configs['windspeed']['pin'], GPIO.IN,
               pull_up_down=GPIO.PUD_UP)
    GPIO.setup(cfg.configs['raingauge']['pin'], GPIO.IN,
               pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(cfg.configs['windspeed']['pin'], GPIO.FALLING)
    GPIO.add_event_callback(cfg.configs['windspeed']['pin'], windEventHandler)

    GPIO.add_event_detect(cfg.configs['raingauge']['pin'], GPIO.FALLING)
    GPIO.add_event_callback(cfg.configs['raingauge']['pin'], rainEventHandler)

    # GPIO.setup(cfg.configs['lightning']['pin'], GPIO.IN)
    # GPIO.add_event_detect(cfg.configs['lightning']['pin'],
    #                       GPIO.RISING, callback=handle_interrupt)

    while True:
        start = datetime.datetime.now()

        # print(sorted(list(data._dumprow)))
        bmp.measure_pressure()
        data.temp = bmp.temperature
        data.pressure = bmp.pressure
        # print("Temperature: " + data.tempF + " deg F")
        # print("Temperature: " + data.tempC + " deg C")
        # print("Pressure : " + data.pressureMillibar + " millibar")
        # print("Pressure : " + data.pressureInchesHG + " inches-Hg")

        (tempc, data.ds18b20temp) = data.ds18b20_read_temp()
        # print("1-wire temp: " + str(data.ds18b20temp))

        humidity, temperature = Adafruit_DHT.read(11, 5)
        if humidity is not None and temperature is not None:
            data.humidityDHT = humidity
            data.temperatureDHT = temperature
            # print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(
            #    temperature, humidity))
        else:
            # if datalast is not None:
            #    humidity = datalast.humidityDHT
            #    temperature = datalast.temperatureDHT
            print('Failed to get reading. Try again!')

        # Analog Readings
        values = [0]*5
        for i in range(5):
            # The read_adc function will get the value
            # of the specified channel (0-7).
            values[i] = mcp.read_adc(i)
        # Print the ADC values.
        # print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |\
# {4:>4} '.format(*range(8)))
#        print('-' * 57)
#        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |\
# {4:>4} '.format(*values))

        data.air1 = values[cfg.configs['air1']['analog-ch']]
        data.air2 = values[cfg.configs['air2']['analog-ch']]
        data.light = values[cfg.configs['lightresistor']['analog-ch']]
        data.soilmoisture = values[cfg.configs['soilmoisture']['analog-ch']]
        data.winddir = values[cfg.configs['winddir']['analog-ch']]
        # print("Wind: " + data.getwinddir(data.winddir))
        # Output:
        now = datetime.datetime.utcnow()
        earlier = datetime.datetime.strptime(data.timeUTC,
                                             '%Y-%m-%d %H:%M:%S.%f')
        # print("St Sec: " + str(e.second) + " " + str(e.microsecond))
        # print("Now   Sec: " + str(now.second) + " " + str(now.microsecond))
        data.tdelta = (now - earlier).total_seconds()
        print("Delta:" + str(data.tdelta))
        print("Data:")
        print(list(data.exportdata()))

        sql = """INSERT into weatherdata (measurement, tdelta, bmp_temp_f,
              bmp_pressuer_millibar, dht_temp_f, dht_humidity_perc,
              light_reading, wind_dir_value, wind_dir_lookup,
              wind_speed_count, rain_count, soil_temp, soil_humidity,
              air_1,  air_2, data_version) values
              (%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"""
        insertdata = list(data.exportdata())

        try:
            cursor.execute(sql, insertdata)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("SQL statement:" + sql)
            print("Data: " + str(insertdata))
            conn.rollback()

        dataout = dataout.writedata(data.exportdata())
        # dataout.fileday = now.day
        # print ("Desc: ")
        # print(data.describedata())
        # datalast = data
        data = WeatherData()
        # time.sleep(0.15)

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
