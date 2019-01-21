<?php
$query = "http://crycharts.stichel.eu/operations.json";
$contents = file_get_contents($query);
echo $contents;
?>
