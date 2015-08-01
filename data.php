<?php
/* Set internal character encoding to UTF-8 */
 mb_internal_encoding("UTF-8");
/* Set output encoding to UTF-8 */
 mb_http_output("UTF-8");
/* übernimmt werte aus create-graph-3.5-dual.html */
$_GET['range'] = diff;
/*echo (diff);
/* berechnet aktuellen Zeitpunkt */
time()*1000 = now;
/* */
  $dbc = mysqli_connect("localhost", "pi", "pi", "klima_growbox");
  $query = "SELECT timestamp,temp1,temp2,temp3,rh1,rh2,rh3,tmax,tmin,absdraussen,absdrinnen FROM daten2 WHERE timestamp > now - diff";
  $data = mysqli_query($dbc, $query);
  $i=0;
  while($row = mysqli_fetch_array($data)){
     $rows[$i]=array($row['timestamp'],$row['temp1'],$row['temp2'],$row['temp3'],$row['rh1'],$row['rh2'],$row['rh3'],$row['tmax'],$row['tmin'],$row['absdraussen'],$row['absdrinnen']);
     $i++;
  }
  echo json_encode($rows, JSON_NUMERIC_CHECK, JSON_UNESCAPED_UNICODE);
?>

