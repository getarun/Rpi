<?php
$plantnumber 	= $_POST["plantnumber"];
$amount      	= $_POST["amount"];
$PH		= $_POST["PH"];
$EC		= $_POST["EC"];
/*
$plantnumber 	= 1;
$amount      	= 500;
$PH		= 5.8;
$EC		= 1.2;
*/
echo "<h1>plantnumber:" . $_POST["plantnumber"] . "</h1>";
$timestamp 	= time()*1000+7200;

  $dbc 		= mysqli_connect("localhost", "pi", "pi", "klima_growbox");
  $query 	= "INSERT INTO klima_growbox.giessen (timestamp,plantnumber,amount,PH,EC) VALUES ($timestamp, $plantnumber, $amount, $PH, $EC)";
  $execute	= mysqli_query($bdc, $query);
  if (mysqli_query($dbc, $query)){
    echo "New record created successfully";
  }
  mysqli_close($dbc);
?>
	
