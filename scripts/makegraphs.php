<?php
$queue = array();

$graphstomake = new stdClass();
$graphstomake->name = "Temperature";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "temperature";
$graphstomake->filenamesuffix = "temp";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "--upper=120 --lower=0";
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "Humidity";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "humidity";
$graphstomake->filenamesuffix = "humidity";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "--upper=100 --lower=0";
$queue[] = $graphstomake;

$graphstomake = new stdClass();
$graphstomake->name = "Pressure";
$graphstomake->datasource = "/usr/local/wun/wundergrounddata.rrd";
$graphstomake->datasourcename = "pressure";
$graphstomake->filenamesuffix = "pressure";
$graphstomake->timeframes = array("1h", "1d", "30d", "1y");
$graphstomake->opts = "";
$queue[] = $graphstomake;




foreach ($queue as $o) {
    foreach ($o->timeframes as $tf){
 `/usr/bin/rrdtool graph /var/www/html/wun/{$o->name}_{$tf}.png --height=200 --width=750 {$o->opts} --title="{$o->name} (last $tf)" --start end-{$tf} DEF:{$o->datasourcename}={$o->datasource}:{$o->datasourcename}:AVERAGE AREA:{$o->datasourcename}#00C000:"{$o->name}"`;
}
}



