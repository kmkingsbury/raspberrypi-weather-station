<?php
$histurl = '/tmp/almanac_Austin.json';
$width = 600;

$queue = array();

$graphstomake = new stdClass();
$graphstomake->name = "Temperature";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "temperature";
$graphstomake->filenamesuffix = "temp";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "--upper=120 --lower=0";
$graphstomake->extra = "GPRINT:{$graphstomake->datasourcename}:LAST:\" Current\:%8.2lf \"  \
		        GPRINT:{$graphstomake->datasourcename}:AVERAGE:\"Average\:%8.2lf \"  \
			GPRINT:{$graphstomake->datasourcename}:MAX:\"Maximum\:%8.2lf \\n\"  ";
$graphstomake->color = "#33CC33";

//Add in Hist
$json = file_get_contents($histurl);
$histobj = json_decode($json,true);
if ( isset( $histobj['almanac']['temp_high']['normal']['F'] ) ) {

  $normalhigh = $histobj['almanac']['temp_high']['normal']['F'];
  $recordhigh = $histobj['almanac']['temp_high']['record']['F'];
  $recordhyear = $histobj['almanac']['temp_high']['recordyear'];

  $normallow = $histobj['almanac']['temp_low']['normal']['F'];
  $recordlow = $histobj['almanac']['temp_low']['record']['F'];
  $recordlyear = $histobj['almanac']['temp_low']['recordyear'];

  $graphstomake->extra .= "HRULE:{$normalhigh}#FF9933:\"Normal High\: {$normalhigh}°F\\n\" ";
  $graphstomake->extra .= "HRULE:{$normallow}#3399FF:\"Normal Low\: {$normallow}°F\\n\" ";
  $graphstomake->extra .= "HRULE:{$recordhigh}#FF0000:\"Record High\: {$recordhigh}°F (in {$recordhyear})\\n\" ";
  $graphstomake->extra .= "HRULE:{$recordlow}#000099:\"Record Low\: {$recordlow}°F (in {$recordlyear})\\n\" ";
 
}
//Now Done
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "Humidity";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "humidity";
$graphstomake->filenamesuffix = "humidity";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "--upper=100 --lower=0";
$graphstomake->extra = "";
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "Pressure";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "pressure";
$graphstomake->filenamesuffix = "pressure";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "";
$graphstomake->extra = "";
$queue[] = $graphstomake;


$graphstomake = new stdClass();
$graphstomake->name = "winddir";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "winddir";
$graphstomake->filenamesuffix = "winddir";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "";
$graphstomake->extra = "";
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "windspeed";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "windspeed";
$graphstomake->filenamesuffix = "windspeed";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "";
$graphstomake->extra = "";
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "rain";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "rain";
$graphstomake->filenamesuffix = "rain";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "";
$graphstomake->extra = "";
$queue[] = $graphstomake;




foreach ($queue as $o) {
    foreach ($o->timeframes as $tf){
     if (!isset($o->color)){
        $o->color = "#0000FF";
     }
 echo `/usr/bin/rrdtool graph /var/www/html/wun/{$o->name}_{$tf}.png \
   --width={$width} {$o->opts} \
   --title="{$o->name} (Last $tf)" \
   --start end-{$tf} \
   DEF:{$o->datasourcename}={$o->datasource}:{$o->datasourcename}:AVERAGE \
   AREA:{$o->datasourcename}{$o->color}:"{$o->name}" \
   {$o->extra}`;
}
}



