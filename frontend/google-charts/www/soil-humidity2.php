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
      data.addColumn('number', 'Soil humidity');

      <?php
      $dbconn = pg_connect("host=weatherstation-mk2 dbname=weatherstation user=weatherstation password=weatherstation")
          or die('Could not connect: ' . pg_last_error());

      // Performing SQL query
      #select * from weatherdata WHERE NOW() > measurement::timestamptz AND NOW() - measurement::timestamptz <= interval '24 hours'
      $query = 'SELECT grid.t5
            ,avg(t.soil_humidity) AS soil

      FROM (
         SELECT generate_series(min(measurement)
                               ,max(measurement), interval \'10 min\') AS t5
         FROM weatherdata
         ) grid
      LEFT JOIN weatherdata t ON t.measurement >= grid.t5
                     AND t.measurement <  grid.t5 +  interval \'10 min\'
      GROUP  BY grid.t5
      ORDER  BY grid.t5 desc limit 1008';
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
            if (strlen($line["soil"])){
              echo $line["soil"];
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
          title: 'Soil Humidity last 7days',
          subtitle: ''
        },
        vAxis: {
            minValue: 0,
            maxValue: 1024,
            viewWindowMode: 'explicit'
            },
        width: 900,
        height: 500
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
