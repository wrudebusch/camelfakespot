<!DOCTYPE html>
<html>
<head>
<title>Table with database</title>
<style>
table {
border-collapse: collapse;
width: 100%;
color: #588c7e;
font-family: monospace;
font-size: 24px;
text-align: left;
}
th {
background-color: #588c7e;
color: white;
}
tr:nth-child(even) {background-color: #f2f2f2}
</style>
</head>
<body>
<table>
<tr>
<th>FS Grade</th>
<th>URL</th>
<th>Current Price</th>
</tr>
<?php

require_once 'config.php';

try {
	$dsn = "pgsql:host=$host;port=5432;dbname=$db;";

	// make a database connection
	$pdo = new PDO(
		$dsn,
		$user,
		$password,
		[PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
	);

	if ($pdo) {
		echo "<br>Connected to the $db database successfully!<br>";
		$data = $pdo->query("SELECT DISTINCT fs_grade, url, product_info, current_price, popular_ts
			FROM popular_and_topdrop
			ORDER BY popular_ts
			LIMIT 100")->fetchAll();
		// and somewhere later:
		foreach ($data as $row) {
		    echo "<tr><td>" . $row['fs_grade'] . "</td><td>" . ' <a href="' . $row['url'] . '">' . $row['product_info'] . '</a> ' . "</td><td>" . $row['current_price'] . "</td></tr>";
		}
	}
} catch (PDOException $e) {
	die($e->getMessage());
}
?>
</table>
</body>
</html>