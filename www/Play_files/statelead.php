<?php

	exec("python ./python/leadstate.py",$out1);	
	echo json_encode($out1);

?> 
