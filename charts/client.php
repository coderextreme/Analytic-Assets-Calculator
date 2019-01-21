<?php
$query = "http://crycharts.stichel.eu/run?".$_SERVER['QUERY_STRING'];
$contents = file_get_contents($query);
# echo $_SERVER['QUERY_STRING'];
# echo "\n";
# echo $query;
echo $contents;
?>
