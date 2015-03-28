<?php
#API
$url = 'http://api.wunderground.com/api/<api_key>/conditions/q/zmw:78701.1.99999.json';
$keyfile = '/etc/wunapikey.txt';
#RRD DB Loc/Name
$rrddb = "/usr/local/wun/wundergrounddata.rrd";

//Makr URL
$apikey = trim(file_get_contents($keyfile));
$url =  str_replace("<api_key>", $apikey, $url);
//echo $url;

//Make API call, decode as Array (true)
$json = file_get_contents($url);
$obj = json_decode($json,true);
//var_dump($obj);

//get our fields:
$temp = $obj['current_observation']['temp_f'];
$humidity = str_replace("%", '', $obj['current_observation']['relative_humidity']);
$winddir = $obj['current_observation']['wind_degrees'];
$windspeed = $obj['current_observation']['wind_mph'];
$pressure = $obj['current_observation']['pressure_mb'];
$rain = $obj['current_observation']['precip_1hr_in'];

//Print.
print "Temp: $temp\n";
print "Humidity: $humidity\n";
print "Wind Dir: $winddir\n";
print "Wind Speed: $windspeed\n";
print "Pressure: $pressure\n";
print "Rain: $rain\n"; 

//update our RRD
echo `/usr/bin/rrdtool update $rrddb N:$temp:$humidity:$winddir:$windspeed:$pressure:$rain`
?>
