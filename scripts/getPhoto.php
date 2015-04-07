<?php
#make this a cron every minute: 
#* * * * * getPhoto.php 

date_default_timezone_set('America/Chicago');

// API
$configs = yaml_parse_file ("/etc/wun/config.yaml");
//var_dump($configs);

$name = date('Y-m-d_h_i') . ".jpg";

$call = "raspistill -o $configs{'photo-location'}.$name"

unlink($configs{'photo-location'}.'current.jpg');
symlink ( $configs{'photo-location'}.$name, $configs{'photo-location'}."current.jpg" );

?>






?>
