<?php
if(array_key_exists('actor_name', $_GET)){
	$actorName = $_GET['actor_name'];
	if(strlen($actorName)> 0){
		$currentPath = getcwd();
		$cmd = "python ".$currentPath."/result.py ".escapeshellarg($actorName);
		passthru($cmd);
		return;
	}
}
?>
<html>
<head>
<title> IMDB Webapp </title>
<style>
body{ background-color: lightgrey;}
form{font-size: 130%; text-align: center; padding-top: 100px;}
input{font-size: 100%;}
</style>
</head>
<body>
<form action="" method="GET">
Name of an actor/actress:
<input type="text" name="actor_name">
<br> <br>
<input type="Submit" value="Submit" function>
</form>
</body>
</html>
