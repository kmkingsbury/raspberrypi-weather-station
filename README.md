# project-template
Template for projects

TODO: Enter the more description here.

# Supported Platforms

TODO: List your supported platforms.

# Contents
Name | Description
-----|------------
`bom.md` | Bill of Materials - List of parts, counts, approximate prices and where to find.
`drawings/`|Mockups, SketchUp Files
`schematics/`| Fritzing Schematics for electronics
`README.md`|This file
`LICENSE`|Apache 2.0 License



## Attributes
Key| Type | Description | Default
---|------|-------------|--------
`-a`| Boolean | whether to include bacon | `true`


# Usage

## default


```json
{
  "item": [
    "otheritem"
  ]
}
```
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
docker build -t gitlab.sigint.cxm:4567/lab-projects/raspberry-pi-weatherstation .

# Components
- Leverages gitlab and pipelines to do tasks
- Started with Database is Postgresql and the pgadmin interface to get GUI
representation.
- Moved to TSDB (Time Series Database) for better trending, anomaly detection, etc.


# License and Authors

Author:: Kevin Kingsbury ([@kmkingsbury](https://twitter.com/kmkingsbury))

Apache 2.0
