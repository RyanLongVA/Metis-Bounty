<!doctype html>
<html lang="en">
  <head>
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
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>BountiesDb Control</title>
    <link href="stylesheets/all.css" rel="stylesheet" type="text/css"/>
    <script src="scripts/jquery.js" rel="javascript/js"></script>

  </head>
  <body>
    <div class="z-depth-3" id="header-container"> 
      <div>Bounties Control</div>
    </div>
    <div id="table-options">
<?php 
 $GrabProgramOptionsStatem = 'SELECT name FROM Programs';
 if (isset($_GET['program'])) {
  $SelectedProgram = $_GET['program'];
  $result = $conn->query("SELECT programId FROM Programs WHERE name = '$SelectedProgram'");
  $row = $result->fetch_row();
  $SelectedProgramId = $row[0];
  // Get the domainRangeIds
  $results2 = $conn->query("SELECT domainRangeId FROM InScope WHERE programId = $SelectedProgramId");
  $rangeIds = array();
  while($row = $results2->fetch_row()) {
    $rangeIds[] = $row[0];
  }

  $result->close();
  $results2->close();
 }
 if (isset($_GET['scoreGreaterThan'])) {
  $ScoreGreaterThan = $_GET['scoreGreaterThan'];
 }
 if (isset($_GET['orderBy'])) {
  $OrderBy = $_GET['orderBy'];
 }

?>
    </div>
    <div id="table-content">

        <?php 

        $PageSize = 20;
        // Getting the page number
        if (isset($_GET['page']) and $_GET['page'] >  0) {
          $PageNumber = $_GET['page'];
        }
        else {
          $PageNumber = 1;
        }
        // Getting the program specifics
        $LimitFloor = $PageSize*($PageNumber-1);
        $LimitCeil = $PageSize*$PageNumber;

        $SqlBase = "SELECT * FROM Domains";
        // Creating the query
        if (isset($SelectedProgram) and isset($ScoreGreaterThan)) {
          // Add both
          $inIds = implode(',', $rangeIds);
          $SqlBase = $SqlBase . " WHERE domainRangeId IN ($inIds) AND RulesScore > $ScoreGreaterThan";
        }
        elseif (isset($SelectedProgram)) {
          $inIds = implode(',', $rangeIds);
          $SqlBase = $SqlBase . " WHERE domainRangeId IN ($inIds)";
        }
        elseif (isset($ScoreGreaterThan)) {
          $SqlBase = $SqlBase . " WHERE RulesScore > $ScoreGreaterThan";
        }
        if (isset($OrderBy)) {
          if ( $OrderBy == 'dateFound') {
          $SqlBase = $SqlBase . " ORDER BY dateFound";
          }
          elseif ($OrderBy == 'domainName') {
            $SqlBase = $SqlBase . " ORDER BY domainName";
          }
        }
        $SqlStatem = $SqlBase . " LIMIT $LimitFloor , $LimitCeil";
        echo $SqlStatem;
        $resultSet = $conn->query($SqlStatem);
        

        // Column titles
        echo "<table border='1'>";
        echo "<tr>";
        echo "<th>domainName</th>";
        echo "<th>dateFound</th>";
        echo "<th>RulesGlobal</th>";
        echo "<th>RulesProgram</th>";
        echo "<th>DateAudited</th>";
        echo "<th>AuditScore</th>";
        echo "<th>RulesScore</th>";
        echo "<th></th>";
        echo "</tr>";
          
        // The form
        echo "<form id='rowSubmit'>";
        while($row = $resultSet->fetch_assoc()) {
          echo "<tr class='z-depth-1 dataRow'>";
          echo "<td class='dataBox'>"."<input type='hidden' name='domainName' value='" . $row['domainName'] . "'/> ". $row['domainName'] . " </td>";
          echo "<td class='dataBox'>"."<input type='hidden' name='dateFound' value='" . $row['dateFound'] . "'/> " . $row['dateFound'] . " </td>";
          echo "<td class='dataBox'>"."<input type='hidden' name='RulesGlobal' value='" . $row['RulesGlobal'] . "'/>" . $row['RulesGlobal'] . " </td>";
          echo "<td class='dataBox'>"."<input type='hidden' name='RulesProgram' value='" . $row['RulesProgram'] . "'/> " . $row['RulesProgram'] . " </td>";
          echo "<td class='dataBox'>"."<input type='hidden' name='DateAudited' value='" . $row['DateAudited'] . "'/> ". $row['DateAudited'] ." </td>";
          echo "<td class='dataBox'>"."<input type='text' name='AuditScore' value='" . $row['AuditScore'] . "'/> </td>";
          echo "<td class='dataBox'>"."<input type='hidden' name='RulesScore' value='" . $row['RulesScore'] . "'/> " . $row['RulesScore'] . " </td>";
          echo "<td class='dataBox'>" . "<input type='submit' name ='update'" . " </td>";
          echo "<input type='hidden' name='domainId'/>";
          echo "</tr>";
        }
        echo "</form>";
        echo "</table>";
        echo $SqlStatem;
        ?>
      </div>
  <script src="scripts/index.js"></script>
  </body>
</html>
