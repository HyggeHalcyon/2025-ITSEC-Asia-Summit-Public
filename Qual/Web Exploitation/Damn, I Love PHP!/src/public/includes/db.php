<?php
$dbFile = __DIR__ . '/../data/database.sqlite';

if (!file_exists($dbFile)) {
    $db = new PDO('sqlite:' . $dbFile);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $db->exec("CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )");
}

function getDb() {
    return new PDO('sqlite:' . __DIR__ . '/../data/database.sqlite');
}
