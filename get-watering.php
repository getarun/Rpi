<?php
/* writes values gives by POST from index.html into DB */
$plantnumber 	= $_POST["plantnumber"];
$amount      	= $_POST["amount"];
$PH		= $_POST["PH"];
$EC		= $_POST["EC"];
/* */
  $timestamp = time()*1000+7200	;
  $dbc 		= mysqli_connect("localhost", "pi", "pi", "klima_growbox");
  $query 	= "INSERT INTO giessen (timestamp,plantnumber,PH,EC) values($timestamp, . $_POST["plantnumber"] ., . $_POST["amount"] ., . $_POST["PH"] ., '" . $_POST["EC"] . "')";
  $insert	= mysqli_query($dbc, $query);
  if (mysqli_affected_rows($insert) > 0) {echo "row inserted"};
?>
