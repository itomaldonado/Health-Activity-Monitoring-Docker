<?php
	header('Content-type:application/json');
	exec("C:\Python34\python PerCapQuery.py",$out1);	
	echo json_encode($out1);
?> 