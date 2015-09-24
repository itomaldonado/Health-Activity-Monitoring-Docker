<?php
	function GetLead($State){
		exec("C:\Python27\python.exe C:\wamp\www\Recommendation_files\temp.py $State",$out2);	
		echo json_encode($out2);
	}

	if(isset($_GET['State'])){
	     GetLead($_GET['State']);
	 }
	else{
	     GetLead('Piscataway');
	}

?> 
