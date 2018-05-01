<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script type="text/javascript">

      google.charts.load('current', {'packages':['line']});
      google.charts.setOnLoadCallback(drawChart);
      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('date', 'Timestamp');
      data.addColumn('number', 'BMP');
      data.addColumn('number', 'DHT');
      data.addColumn('number', 'Soil');
      data.addColumn('number', 'Pressure');
      <?php
      $dbconn = pg_connect("host=weatherstation-mk2 dbname=weatherstation user=weatherstation password=weatherstation")
          or die('Could not connect: ' . pg_last_error());

      // Performing SQL query
      #select * from weatherdata WHERE NOW() > measurement::timestamptz AND NOW() - measurement::timestamptz <= interval '24 hours'
      $query = 'SELECT grid.t5
            ,avg(t.bmp_temp_f) AS bmptemp
            ,avg(t.dht_temp_f) AS dhttemp
            ,avg(t.soil_temp) AS soiltemp
            ,avg(t.bmp_pressuer_millibar) AS pressure
      FROM (
         SELECT generate_series(min(measurement)
                               ,max(measurement), interval \'10 min\') AS t5
         FROM weatherdata
         ) grid
      LEFT JOIN weatherdata t ON t.measurement >= grid.t5
                     AND t.measurement <  grid.t5 +  interval \'10 min\'
      GROUP  BY grid.t5
      ORDER  BY grid.t5 desc limit 1440';
      $result = pg_query($query) or die('Query failed: ' . pg_last_error());
      ?>
      data.addRows([
        <?php
        $rows = pg_num_rows($result);
        $c = 0;
        while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
            $c++;
           #echo "data.addRow([";
            preg_match('/(\d{4})\-(\d{2})\-(\d{2})\s+(\d{2})\:(\d{2})\:(.*)/i', $line["t5"], $d);
            echo "[ new Date(Date.UTC($d[1], $d[2]-1, $d[3], $d[4], $d[5]))";
            echo ", ";
            if (strlen($line["bmptemp"])){
              echo $line["bmptemp"];
            } else {
              echo "null";
            }
            echo ", ";
            if (strlen($line["dhttemp"])){
            echo $line["dhttemp"];
            } else {
              echo "null";
            }
            echo ", ";
            if (strlen($line["soiltemp"])){
              echo $line["soiltemp"];
            } else {
              echo "null";
            }
            echo ", ";
            if (strlen($line["pressure"])){
              echo $line["pressure"];
            } else {
              echo "null";
            }
            echo "]";
            #echo "#  ".$line["measurement"];
            if ($c < $rows){
              echo ",\n";
            }
        }
        ?>
      ]);
      var options = {
        chart: {
          title: 'Temperature last 24hrs',
          subtitle: 'in degrees Fahrenheit'
        },
        width: 900,
        height: 500,
        series: {
          // Gives each series an axis name that matches the Y-axis below.
          0: {axis: 'Temps'},
          1: {axis: 'Temps'},
          2: {axis: 'Temps'},
          3: {axis: 'Pressure'}
        },
        axes: {
          // Adds labels to each axis; they don't have to match the axis names.
          y: {
            Temps: {label: 'Temps (Fahrenheit)'},
            Pressure: {label: 'Pressure'}
          }
        }
      };

      var chart = new google.charts.Line(document.getElementById('chart_div'));

      chart.draw(data, google.charts.Line.convertOptions(options));
    }
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <div id="chart_div"></div>
  </body>
</html>
