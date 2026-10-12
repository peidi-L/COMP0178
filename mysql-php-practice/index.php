<?php
declare(strict_types=1);

$host = getenv('MYSQL_HOST') ?: '127.0.0.1';
$port = getenv('MYSQL_PORT') ?: '3306';
$database = getenv('MYSQL_DATABASE') ?: 'EstateAgent';
$user = getenv('MYSQL_USER') ?: 'root';
$password = getenv('MYSQL_PASSWORD');

if ($password === false) {
    http_response_code(500);
    exit('Set MYSQL_PASSWORD before starting the PHP server.');
}

try {
    $pdo = new PDO(
        "mysql:host={$host};port={$port};dbname={$database};charset=utf8mb4",
        $user,
        $password,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );

    $staff = $pdo->query(
        'SELECT s.staffNo, s.fName, s.lName, s.position, b.city
         FROM Staff AS s
         LEFT JOIN Branch AS b ON s.branchNo = b.branchNo
         ORDER BY s.staffNo'
    )->fetchAll();
} catch (PDOException $error) {
    http_response_code(500);
    exit('Database connection failed: ' . htmlspecialchars($error->getMessage()));
}
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>EstateAgent staff</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 850px; margin: 3rem auto; padding: 0 1rem; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #bbb; padding: .6rem; text-align: left; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1>EstateAgent staff</h1>
    <p>PHP retrieved <?= count($staff) ?> row(s) from MySQL.</p>
    <table>
        <thead><tr><th>Staff number</th><th>Name</th><th>Position</th><th>Branch city</th></tr></thead>
        <tbody>
        <?php foreach ($staff as $member): ?>
            <tr>
                <td><?= htmlspecialchars($member['staffNo']) ?></td>
                <td><?= htmlspecialchars($member['fName'] . ' ' . $member['lName']) ?></td>
                <td><?= htmlspecialchars($member['position'] ?? '') ?></td>
                <td><?= htmlspecialchars($member['city'] ?? 'Unassigned') ?></td>
            </tr>
        <?php endforeach; ?>
        </tbody>
    </table>
</body>
</html>

