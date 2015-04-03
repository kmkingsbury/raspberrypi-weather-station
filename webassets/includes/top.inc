<?php

function Print_Head($sunrise, $sunset){
?>
<html>
<head>
<title>Title Here</title>
<link rel="stylesheet" type="text/css" href="main.css">
<style>
<?php

$now = strtotime("now");
$sunrisetime = strtotime($sunrise . " AM");
$sunsettime = strtotime($sunset . " PM");
#print "Now: $now\n Sunrise: $sunrisetime\n Sunset: $sunsettime\n";

$diff = (60*60*2);

if ($now >= ($sunrisetime - $diff) && $now <= ($sunrisetime + $diff)){
 print "html {\n background-image: url('img/sunrise.png');\n}\n";						  
} elseif ($now >= ($sunrisetime + $diff) && $now <= ($sunsettime - $diff)){
 print "html {\n background-image: url('img/day.png');\n}\n";						  
} elseif ($now >= ($sunsettime - $diff) && $now <= ($sunsettime + $diff)){
 print "html {\n background-image: url('img/sunset.png');\n}\n";						  
} else {
 print "html {\n background-image: url('img/night.png');\n}\n";						  
}

?></style>
</head>
<body>
<?php
echo "<!-- body -->";
}
?>
