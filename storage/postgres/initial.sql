CREATE TABLE weatherdata (
measurement timestamp NOT NULL,
bmp_temp_f varchar(20) NOT NULL,
bmp_pressuer_millibar text NOT NULL,
dht_temp_c datetime default NULL,
dht_humidity_perc,
light_reading,
wind_dir_value default 0,
wind_speed_count default 0,
rain_count default 0,
soil_temp,
soil_humidity,
air_1,
air_2,
PRIMARY KEY (measurement)
);
