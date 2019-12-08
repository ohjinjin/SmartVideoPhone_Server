<?php
 
// Create connection
$con=mysqli_connect("localhost","root","","smartvideophone");
 
// Check connection
if (mysqli_connect_errno($con))
{
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
 
// Select all of our stocks from table 'stock_tracker'
$sql = "SELECT * FROM visit_log";
$res = mysqli_query($con, $sql);

// Confirm there are results
$result = array();
while ($row = mysqli_fetch_array($res))
{
	array_push($result, array('visit_date'=>$row[0],'image'=>$row[1])); 
}
echo json_encode(array("result"=>$result), JSON_UNESCAPED_UNICODE);

// Close connections
mysqli_close($con);
?>