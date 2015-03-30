<?php
$configs = yaml_parse_file ("./config.yaml");




$width = 600;
$days = array("1h", "1d", "7d", "30d", "1y");

$queue = array();

$graphstomake = new stdClass();
$graphstomake->name = "Temperature";
$graphstomake->datasource = $configs{'rrddb'};
$graphstomake->datasourcename = "temperature";
$graphstomake->filenamesuffix = "temp";
$graphstomake->timeframes = $days;
$graphstomake->opts = "";
$graphstomake->extra = "GPRINT:{$graphstomake->datasourcename}:LAST:\" Current\:%8.2lf \"  \
		        GPRINT:{$graphstomake->datasourcename}:AVERAGE:\"Average\:%8.2lf \"  \
			GPRINT:{$graphstomake->datasourcename}:MAX:\"Maximum\:%8.2lf \" \
 			GPRINT:{$graphstomake->datasourcename}:MIN:\"Minimum\:%8.2lf \\n\"  "; 
$graphstomake->color = "#33CC33";

//Add in Hist
$json = file_get_contents($configs{'history-file-location'});
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
$graphstomake->datasource = $configs{'rrddb'};
$graphstomake->datasourcename = "humidity";
$graphstomake->filenamesuffix = "humidity";
$graphstomake->timeframes = $days;
$graphstomake->opts = "--upper=100 --lower=0";
$graphstomake->extra = "";
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "Pressure";
$graphstomake->datasource = $configs{'rrddb'};
$graphstomake->datasourcename = "pressure";
$graphstomake->filenamesuffix = "pressure";
$graphstomake->timeframes = $days;
$graphstomake->opts = "";
$graphstomake->extra = "";
$queue[] = $graphstomake;


$graphstomake = new stdClass();
$graphstomake->name = "winddir";
$graphstomake->datasource = $configs{'rrddb'};
$graphstomake->datasourcename = "winddir";
$graphstomake->filenamesuffix = "winddir";
$graphstomake->timeframes = $days;
$graphstomake->opts = "";
$graphstomake->extra = "";
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "windspeed";
$graphstomake->datasource = $configs{'rrddb'};
$graphstomake->datasourcename = "windspeed";
$graphstomake->filenamesuffix = "windspeed";
$graphstomake->timeframes = $days;
$graphstomake->opts = "";
$graphstomake->extra = "";
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "rain";
$graphstomake->datasource = $configs{'rrddb'};
$graphstomake->datasourcename = "rain";
$graphstomake->filenamesuffix = "rain";
$graphstomake->timeframes = $days;
$graphstomake->opts = "";
$graphstomake->extra = "";
$queue[] = $graphstomake;




foreach ($queue as $o) {
    foreach ($o->timeframes as $tf){
     if (!isset($o->color)){
        $o->color = "#0000FF";
     }
 echo `/usr/bin/rrdtool graph {$configs{'graph-location'}}{$o->name}_{$tf}.png \
   --width={$width} {$o->opts} \
   --title="{$o->name} (Last $tf)" \
   --start end-{$tf} \
   DEF:{$o->datasourcename}={$o->datasource}:{$o->datasourcename}:AVERAGE \
   AREA:{$o->datasourcename}{$o->color}:"{$o->name}" \
   {$o->extra}`;
}
}



