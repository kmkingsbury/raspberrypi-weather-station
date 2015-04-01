<?php

// API
$configs = yaml_parse_file ("./config.yaml");
//var_dump($configs);

// Add trailing slash if missing
if (substr($configs{'archive-location'}, -1) != "/"){
   $configs{'archive-location'} . "/";
}
$apikey = trim(file_get_contents($configs{'wun-api-keyfile'}));




$history = $configs{'archive-location'}.$configs{'history-file'};
$astronomy = $configs{'archive-location'}.$configs{'astronomy-file'};

$files = array();
$files[0] = array('name'=>'almanac', 'file'=>$history, 'url'=>$configs{'wun-almanac-url'});	   
$files[1] = array('name'=>'astronomy', 'file'=>$astronomy, 'url'=>$configs{'wun-astronomy-url'});	   
foreach ($files as $f){
	$url =  str_replace("<api_key>", $apikey, $f['url']);
	$url =  str_replace("<state>", $configs{'wun-api-location-state'}, $url);
	$url =  str_replace("<city>", $configs{'wun-api-location-city'}, $url);

	print "URL:" . $url;

	$tuCurl = curl_init(); 
	curl_setopt($tuCurl, CURLOPT_URL, $url); 
	
	$tuData = curl_exec($tuCurl); 
	if(!curl_errno($tuCurl)){ 
	  $info = curl_getinfo($tuCurl); 
	  echo 'Took ' . $info['total_time'] . ' seconds to send a request'; #to ' . $info['url']; 
	} else { 
	  echo 'Curl error: ' . curl_error($tuCurl); 
	} 

	//archive-loc
	print "File:". $configs{'archive-location'}.$f['name']."_".strtolower($configs{'wun-api-location-city'})."_".date('Y-m-d').".json";
	$fp = fopen($configs{'archive-location'}.$f['name']."_".strtolower($configs{'wun-api-location-city'})."_".date('Y-m-d').".json", 'w');
	fwrite($fp, $tuData);
	fclose($fp);
	curl_close($tuCurl); 

	// relink
	unlink($f['file']);
	symlink ( $configs{'archive-location'}.$f['name']."_".strtolower($configs{'wun-api-location-city'})."_".date('Y-m-d').".json" , $f['file'] );

}





?>
