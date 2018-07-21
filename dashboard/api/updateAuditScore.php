<?php 
    // Globals
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "bounties2";
    
    // Creating database class
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }
    if(isset($_POST['AuditScore']) and isset($_POST['domainName'])) {
    	$SqlStatem = "UPDATE `Domains` SET AuditScore = " . $_POST['AuditScore'] . ", DateAudited = CURDATE() WHERE domainName = '" . $_POST['domainName'] . "'";
    	if ($conn->query($SqlStatem) === TRUE) {
    		echo "Record updated successfully";
		} else {
    		echo "Error updating record: " . $conn->error;
		}
    }
?>