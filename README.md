# raspberry-pi-weatherstation

Rebuild of a Pi powered weather station. The origial I did an instructable for (https://www.instructables.com/id/Complete-DIY-Raspberry-Pi-Weather-Station-with-Sof/) this one uses all off the self parts.

And wrote up a few thoughts about the project on my blog as well: 
https://spaceman-labs.com/2018/07/raspberry-pi-weather-station-mk2/

Uses a few standard sensors to track weather data:
- Temperature - comes from 2 sensors the BMP and the DHT.
- Soil temperature
- Soil humidity
- Light - via a photoresistor. The Higher the number the darker out.
- Pressure
- Humidity
- 2 Air sensors - One does more dust and smoke, air quality. The other looks for gases like propane and butane.
- Wind speed
- Wind dir
- Rain Gauge
- Lightning detector - Currently having issues so commented out.

The analog sensors run through the MCP3008 chip to get converted to a digital reading.

The wiring and circuit boards are in the schematics directory and is a Fritzing file. There are also PDFs I used to print the PCB to thermal transfer paper and burn the Copper circuit boards. There are two boards: 1 in the main station for the MCP3008 A/D converter and photo resistor, and the 2nd is a "remote" unit that goes in the Amrite housing and does the air sensing, pressure, temp, and humidity, via 2 air sensors, the DHT, and the BMP.

Data is logged to a postgres table as well as a CSV file and the CSV file is rotated out nightly. The log file also contains some of the data and other debug statements.

Some frontend code is supplied to display/graph the data using Google Charts. This uses PHP to write javascript code, so it's far from ideal.
Also needs more reusable code, since a bug or change needs to go across all the pages and I've currently not been fixing that. Timeframes are roughly 24 hrs and 7-days (for the files ending in 2). Currently very buggy and titles/labels aren't very accurate (months in javascript start at 0 not 1). Will probably rewrite the frontend to something like NodeJS that will integrate easier with Google Charts (or another plotting package)

I used Gitlab and gitlab pipelines to do some automated CI and testing so the gitlab-ci is provided for some of that.


# Contents
Name | Description
-----|------------
`bom.md` | Bill of Materials - List of parts, counts, approximate prices and where to find.
`schematics/`| Fritzing Schematics for electronics
`station-code/`| Python3 Code.
`station-code/collectweather.py`| Main code for collecting weather data.
`README.md`|This file
`LICENSE`|Apache 2.0 License
`frontend/`| Docker container from running PHP scripts to display the data.
`structure.sql` | Postgresql Data schema.



# Pi Setup
- apt-get update
- apt-get upgrade
- apt-get dist-upgrade
- apt-get autoremove
- Turn on Interfacing Options:
    - SPI
    - I2C
    - 1-wire


# Python Packages
- sudo apt-get install libyaml-dev
- pip3 install pyyaml
- pip3 install structlog
- pip3 install numpy
- sudo apt-get install build-essential python-dev python3-dev
- sudo pip install psycopg2

# Postgresql Setup
- sudo apt-get install postgresql-9.6
- apt install postgresql libpq-dev postgresql-client postgresql-client-common
- sudo update-rc.d postgresql enable
- sudo su postgres
- createuser weatherstation -P --interactive
- createdb weatherstation
- create table using structure.sql
- GRANT ALL PRIVILEGES ON TABLE weatherdata TO weatherstation;
- https://www.howtoforge.com/tutorial/postgresql-replication-on-ubuntu-15-04/

# 3rd Party Sensor Modules:
Add SSH key:
```
eval $(ssh-agent -s)
ssh-add ~/.ssh/other_id_rsa
```
Checkout Modules, run sudo python setup.py install
```
git clone https://github.com/PrzemoF/bmp183.git
git clone git://gist.github.com/3151375.git
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
```

Docker testing image:
```
docker build -t gitlab:4567/lab-projects/raspberry-pi-weatherstation .
```

# Components
- Leverages gitlab and pipelines to do tasks
- Started with Database is Postgresql and the pgadmin interface to get GUI
representation.



# License and Authors

Author:: Kevin Kingsbury ([@kmkingsbury](https://twitter.com/kmkingsbury))

Apache 2.0
