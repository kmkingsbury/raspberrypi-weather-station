<?php

# // -c for config
$shortopts  = "";
$shortopts .= "c:"; //required config

// for --config
$longopts  = array(
    "config:",     // Required value
    "optional::",    // Optional value
);
$options = getopt($shortopts, $longopts);
//var_dump($options);


#test, if (! $c or ! $config) then abort!
$configs = yaml_parse_file ("./config.yaml");
var_dump($configs);
?>
