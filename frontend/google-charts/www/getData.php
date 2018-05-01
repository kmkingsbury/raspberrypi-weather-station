<?php

// This is just an example of reading server side data and sending it to the client.
// It reads a json formatted text file and outputs it.

#$string = file_get_contents("sampleData.json");
#echo $string;

// Instead you can query your database and parse into JSON etc etc

// Connecting, selecting database
$dbconn = pg_connect("host=weatherstation-mk2 dbname=weatherstation user=weatherstation password=weatherstation")
    or die('Could not connect: ' . pg_last_error());

// Performing SQL query
$query = 'SELECT bmp_temp_f FROM weatherdata limit 1';
$result = pg_query($query) or die('Query failed: ' . pg_last_error());

// Printing results in HTML
#echo "<table>\n";
echo "{\n";
echo "\"cols\": [\n";
echo "{\"id\":\"\",\"label\":\"Temperature BMP\",\"pattern\":\"\",\"type\":\"string\"},\n";
#        {"id":"","label":"Slices","pattern":"","type":"number"}
echo "],\n";
echo "\"rows\": [\n";
      {"c":[{"v":"Mushrooms","f":null},{"v":3,"f":null}]},

while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
    echo "\t<tr>\n";
    foreach ($line as $col_value) {
        echo "\t\t<td>$col_value</td>\n";
    }
    echo "\t</tr>\n";
}
echo "</table>\n";

// Free resultset
pg_free_result($result);

// Closing connection
pg_close($dbconn);
?>
