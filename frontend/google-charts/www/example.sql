

SELECT grid.t5
      ,min(t.measurement) AS min_time
--    ,array_agg(extract(min FROM t."time")) AS 'players_on' -- optional
      ,avg(t.bmp_temp_f) AS bmptemp
      ,avg(t.dht_temp_f) AS dtemp
      ,avg(t.soil_temp) AS stemp

--      ,avg(t.servers) AS avg_servers
FROM (
   SELECT generate_series(min(measurement)
                         ,max(measurement), interval '1 min') AS t5
   FROM weatherdata
   ) grid
LEFT JOIN weatherdata t ON t.measurement >= grid.t5
               AND t.measurement <  grid.t5 +  interval '1 min'
GROUP  BY grid.t5
ORDER  BY grid.t5 desc limit 1440;
