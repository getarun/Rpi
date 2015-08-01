<?php
/* */
  $dbc = mysqli_connect("localhost", "pi", "pi", "klima_growbox");
  $query = "SELECT timestamp,temp1,temp2,temp3,rh1,rh2,rh3,tmax,tmin,absdraussen,absdrinnen FROM daten";
  $data = mysqli_query($dbc, $query);
  $i=0;
  while($row = mysqli_fetch_array($data)){
     $rows[$i]=array($row['timestamp'],$row['temp1'],$row['temp2'],$row['temp3'],$row['rh1'],$row['rh2'],$row['rh3'],$row['tmax'],$row['tmin'],$row['absdraussen'],$row['absdrinnen']);
     $i++;
  }
  echo json_encode($rows, JSON_NUMERIC_CHECK);
?>

