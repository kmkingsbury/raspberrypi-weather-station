CREATE TABLE weatherdata (
measurement timestamp NOT NULL,
bmp_temp_f NUMERIC(5,2) NOT NULL,
bmp_pressuer_millibar NUMERIC(5,2) NOT NULL,
dht_temp_c NUMERIC(5,2) NOT NULL,
dht_humidity_perc NUMERIC(5,2) NOT NULL,
light_reading NUMERIC(5,2) NOT NULL,
wind_dir_value NUMERIC(5,2) NOT NULL,
wind_speed_count smallint default 0,
rain_count smallint default 0,
soil_temp NUMERIC(5,2) NOT NULL,
soil_humidity NUMERIC(5,2) NOT NULL,
air_1 NUMERIC(5,2) NOT NULL,
air_2 NUMERIC(5,2) NOT NULL,
data_version smallint,
PRIMARY KEY (measurement)
);
