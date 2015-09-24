<?php
	header('Content-type:application/json');	
	$item = '[{"lat":3,"log":100},
	{"lat":6,"log":101},
	{"lat":4,"log":120},
	{"lat":8,"log":160}]';
	//$item = 15;
	echo json_encode($item);
?> 