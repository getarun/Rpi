<?php
/* */
  $dbc = mysqli_connect("localhost", "pi", "pi", "klima_growbox");
  $query = "SELECT timestamp,PH,EC FROM giessen";
  $data = mysqli_query($dbc, $query);
  $i=0;
  while($row = mysqli_fetch_array($data)){
     $rows[$i]=array($row['timestamp'],$row['PH'],$row['EC']);
     $i++;
  }
  echo json_encode($rows, JSON_NUMERIC_CHECK);
?>
