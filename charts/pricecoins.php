<?php
$query = "http://crycharts.stichel.eu/pricecoins.json";
$contents = file_get_contents($query);
echo $contents;
?>
