<?php
	function GetLead($State){
		exec("python ./python/leadcity.py $State",$out2);	
		echo json_encode($out2);
	}

	if(isset($_GET['State'])){
	     GetLead($_GET['State']);
	 }
	else{
	     GetLead('NJ');
	}

?> 
