<?php
$PH		= $_POST["PH"];
$EC		= $_POST["EC"];

$plantnumber 	= 1;
$amount      	= 5;
/*
$PH		= 5.8;
$EC		= 1.2;
*/
echo "<h1>PH:" . $_POST["PH"] . ", EC:" . $_POST["EC"] . "</h1>";

$timestamp 	= time()*1000+7200;

  $dbc 		= mysqli_connect("localhost", "pi", "pi", "klima_growbox");
  $query 	= "INSERT INTO klima_growbox.giessen (timestamp,plantnumber,amount,PH,EC) VALUES ($timestamp, $plantnumber, $amount, $PH, $EC)";
  $execute	= mysqli_query($bdc, $query);
  if (mysqli_query($dbc, $query)){
	echo "<script type="text/javascript">alert("PH: ".$PH." EC: " .$EC. "in Datenbank gespeichert (" .$timestamp. ")");</script>";
  }
  mysqli_close($dbc);
?>
	
