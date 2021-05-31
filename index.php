<?php echo date('Y-m-d H:i:s'); ?>
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
		$data = $pdo->query("SELECT * 
			FROM popular_and_topdrop
			ORDER BY popular_ts, fs_grade
			LIMIT 100")->fetchAll();
		// and somewhere later:
		foreach ($data as $row) {
		    echo $row['fs_grade'] . ' <a href="' . $row['url'] . '">' . $row['product_info'] . '</a> ' . $row['current_price'] . '<br>';
		}
	}
} catch (PDOException $e) {
	die($e->getMessage());
}
?>