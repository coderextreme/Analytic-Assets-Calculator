<?php
$query = "http://crycharts.stichel.eu/amountcoins.json";
$contents = file_get_contents($query);
echo $contents;
?>
