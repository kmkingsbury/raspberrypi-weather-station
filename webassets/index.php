<?php
date_default_timezone_set('America/Chicago');



//Get old data:
$json = file_get_contents('./archive/almanac_current.json');
$archiveobj = json_decode(trim($json),true);


$json = file_get_contents('./archive/astronomy_current.json');
$astroobj = json_decode(trim($json),true);

$sunrise = $astroobj['sun_phase']['sunrise']['hour'] . ":" . $astroobj['sun_phase']['sunrise']['minute'];
$sunset = $astroobj['sun_phase']['sunset']['hour'] . ":" . $astroobj['sun_phase']['sunset']['minute'];
$sunset = Date('g:i', strtotime ($sunset));

// Get Data
#//rrdtool fetch /usr/local/wun/wundergrounddata.rrd AVERAGE -r 300 -s -10min -e -5min

$result = rrd_fetch( "./wundergrounddata.rrd", array( "AVERAGE", "--resolution", "300", "--start", "-10min", "--end", "-5min" ) );
//$a = print_r($result);
//print "<pre>T: ". print_r($result['data']['temperature'], true);

$data = array();
$data['temperature'] = 0;
$data['humidity'] = 0;
$data['winddir'] = 0;
$data['windspeed'] = 0;
$data['pressure'] = 0;
$data['rain'] = 0;

foreach ($data as $key=>$value){

	foreach ( $result['data'][$key] as $otherkey => $value )
	{	
	    if (strcmp($value, "NAN") != 0){
	           $data[$key] = $value;
       	    }     	   
	}
}
print rrd_error();


include('includes/top.inc');
print_Head($sunrise, $sunset, $data['temperature'] );

?>
<script type="text/javascript">
 function changeImage(element) {
   document.getElementById('imageReplace').src = element; 
 }
</script>

<script type="text/javascript">
 function changeImage2(element) {
   document.getElementById('imageReplace2').src = element; 
 }
</script>

<script type="text/javascript">
 function changeImage3(element) {
   document.getElementById('imageReplace3').src = element; 
 }
</script>

<script type="text/javascript">
 function changeImage4(element) {
   document.getElementById('imageReplace4').src = element; 
 }
</script>

<script type="text/javascript">
 function changeImage5(element) {
   document.getElementById('imageReplace5').src = element; 
 }
</script>

<script type="text/javascript">
 function changeImage6(element) {
   document.getElementById('imageReplace6').src = element; 
 }
</script>

<?php




$sunset = $astroobj['sun_phase']['sunset']['hour'] . ":" . $astroobj['sun_phase']['sunset']['minute'];
$sunset = Date('g:i', strtotime ($sunset));

$moon =  $astroobj['moon_phase']['ageOfMoon'];
$total = 29.5;

//$img = round((($moon) * $total) / 24);
$img = $moon;
if ($moon < 16){
 $img = $img - 2;
} else {
  $img = $img - 3;
}
if ($img < 0 ){ $img =0; }
if ($img > 24  ){ $img  = 24; }

?>
<div id="container">
     <header>Topper </header>
          <section>
		<div style="float: left"><h2><?php echo sprintf("%0.1f", $data['temperature']); ?>&deg;F</h2>Sunrise: <?php print $astroobj['sun_phase']['sunrise']['hour'] . ":" . $astroobj['sun_phase']['sunrise']['minute'];?> AM<br/>Sunset: <?php print $sunset; ?> PM</div>

	<div style="float: right; text-align: center;"><img src="img/<?php echo $img; ?>.jpg" width="150"><br clear="all"><span><?php print $astroobj['moon_phase']['phaseofMoon']; ?><br><?php print "Age of Moon:". $moon . " days"; ?></span></div>	  
    	  </section>
     	  <aside>
		<table>
		  <tr>
 		    <td>Humidity:</td><td><strong><?php echo sprintf("%0.1f", $data['humidity']); ?>%</strong></td>
		  </tr>
		  <tr>
 		    <td>Pressure:</td><td><strong><?php echo sprintf("%0.1f", $data['pressure']); ?> mb</strong></td>
		  </tr>
		  <tr>
 		    <td>Rainfall:</td><td><strong><?php echo sprintf("%0.1f", $data['rain']); ?> in</strong></td>
		  </tr>
		  <tr>
 		    <td>Light:</td><td><strong>--</strong></td>
		  </tr>
		</table>
 </aside>
     <article><h3>Latest Img:</h3></article> 
     <article>
     <h3>Temperature:</h3><span style="display: block; text-align: right">
<a href="#t" onclick="changeImage('wun/Temperature_1h.png?'+Math.random());">1h</a>
<a href="#t" onclick="changeImage('wun/Temperature_1d.png?'+Math.random());">1d</a>
<a href="#t" onclick="changeImage('wun/Temperature_7d.png?'+Math.random());">7d</a>
<a href="#t" onclick="changeImage('wun/Temperature_30d.png?'+Math.random());">30d</a>
<a href="#t" onclick="changeImage('wun/Temperature_1y.png?'+Math.random());">1y</a></span>
<a name="t"><img src="wun/Temperature_1d.png" alt="Temperature Graph" id="imageReplace"/></a><br />

     <h3>Humidity:</h3><span style="display: block; text-align: right">
<a href="#h" onclick="changeImage2('wun/Humidity_1h.png?'+Math.random());">1h</a>
<a href="#h" onclick="changeImage2('wun/Humidity_1d.png?'+Math.random());">1d</a>
<a href="#h" onclick="changeImage2('wun/Humidity_7d.png?'+Math.random());">7d</a>
<a href="#h" onclick="changeImage2('wun/Humidity_30d.png?'+Math.random());">30d</a>
<a href="#h" onclick="changeImage2('wun/Humidity_1y.png?'+Math.random());">1y</a></span>
<a name="h"><img src="wun/Humidity_1d.png" alt="Humidity Graph" id="imageReplace2"/></a><br />

     <h3>Pressure:</h3><span style="display: block; text-align: right">
<a href="#p" onclick="changeImage3('wun/Pressure_1h.png?'+Math.random());">1h</a>
<a href="#p" onclick="changeImage3('wun/Pressure_1d.png?'+Math.random());">1d</a>
<a href="#p" onclick="changeImage3('wun/Pressure_7d.png?'+Math.random());">7d</a>
<a href="#p" onclick="changeImage3('wun/Pressure_30d.png?'+Math.random());">30d</a>
<a href="#p" onclick="changeImage3('wun/Pressure_1y.png?'+Math.random());">1y</a></span>
<a name="p"><img src="wun/Pressure_1d.png" alt="Pressure Graph" id="imageReplace3"/></a><br />

     <h3>Rain:</h3><span style="display: block; text-align: right">
<a href="#r" onclick="changeImage4('wun/rain_1h.png?'+Math.random());">1h</a>
<a href="#r" onclick="changeImage4('wun/rain_1d.png?'+Math.random());">1d</a>
<a href="#r" onclick="changeImage4('wun/rain_7d.png?'+Math.random());">7d</a>
<a href="#r" onclick="changeImage4('wun/rain_30d.png?'+Math.random());">30d</a>
<a href="#r" onclick="changeImage4('wun/rain_1y.png?'+Math.random());">1y</a></span>
<a name="r"><img src="wun/rain_1d.png" alt="Rain Graph" id="imageReplace4"/></a><br />

     <h3>Wind Direction:</h3><span style="display: block; text-align: right">
<a href="#wd" onclick="changeImage5('wun/winddir_1h.png?'+Math.random());">1h</a>
<a href="#wd" onclick="changeImage5('wun/winddir_1d.png?'+Math.random());">1d</a>
<a href="#wd" onclick="changeImage5('wun/winddir_7d.png?'+Math.random());">7d</a>
<a href="#wd" onclick="changeImage5('wun/winddir_30d.png?'+Math.random());">30d</a>
<a href="#wd" onclick="changeImage5('wun/winddir_1y.png?'+Math.random());">1y</a></span>
<a name="wd"><img src="wun/winddir_1d.png" alt="Wind Speed Graph" id="imageReplace5"/></a><br />

     <h3>Wind Speed:</h3><span style="display: block; text-align: right">
<a href="#ws" onclick="changeImage6('wun/windspeed_1h.png?'+Math.random());">1h</a>
<a href="#ws" onclick="changeImage6('wun/windspeed_1d.png?'+Math.random());">1d</a>
<a href="#ws" onclick="changeImage6('wun/windspeed_7d.png?'+Math.random());">7d</a>
<a href="#ws" onclick="changeImage6('wun/windspeed_30d.png?'+Math.random());">30d</a>
<a href="#ws" onclick="changeImage6('wun/windspeed_1y.png?'+Math.random());">1y</a></span>
<a name="ws"><img src="wun/windspeed_1d.png" alt="Wind Speed Graph" id="imageReplace6"/></a><br />


     </article> 
     <footer>Bottom</footer>
</div>
<?php
include('includes/bottom.inc');
?>
