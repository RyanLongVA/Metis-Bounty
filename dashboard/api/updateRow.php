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
?>