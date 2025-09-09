<?php

require_once __DIR__ . '/db.php';
require_once __DIR__ . '/functions.php';

$action = $_GET['action'] ?? 'home';

switch ($action) {
    case 'register':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $username = $_POST['username'] ?? '';
            $password = password_hash($_POST['password'] ?? '', PASSWORD_BCRYPT);

            try {
                $db = getDb();
                $stmt = $db->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
                $stmt->execute([$username, $password]);
                echo "Register successful. <a href='?action=login'>Login</a>";
            } catch (Exception $e) {
                echo "Error: " . escape($e->getMessage());
            }
            exit;
        }
        break;

    case 'login':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $username = $_POST['username'] ?? '';
            $password = $_POST['password'] ?? '';

            $db = getDb();
            $stmt = $db->prepare("SELECT * FROM users WHERE username = ?");
            $stmt->execute([$username]);
            $user = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($user && password_verify($password, $user['password'])) {
                $_SESSION['user'] = $user;
                echo "Login successful. <a href='?action=dashboard'>Dashboard</a>";
            } else {
                echo "Login failed.";
            }
            exit;
        }
        break;

    case 'dashboard':
        if (isset($_SESSION['user'])) {
            require_once __DIR__ . '/header.php';

            $username = escape($_SESSION['user']['username']);
            $role = $_SESSION['user']['role'] ?? '';
            $isAdmin = stripos($role, 'admin') !== false;

            $badgeClass = $isAdmin ? 'bg-success' : 'bg-danger';
            $adminStatus = $isAdmin ? '✅ Yes' : '❌ No';

            echo <<<HTML
    <div class="container my-5 dashboard">
        <div class="card shadow-lg">
            <div class="card-body">
                <h2 class="card-title mb-4">Welcome, <span class="text-primary">{$username}</span></h2>

                <div class="mb-4">
                    <p><strong>Your Role:</strong> <span class="badge bg-secondary">{$role}</span></p>
                    <p><strong>Admin Access:</strong> <span class="badge {$badgeClass}">{$adminStatus}</span></p>
                </div>

                <div class="mb-4">
                    <h4>Change Your Role</h4>
                    <form method="POST" action="?action=change-role" class="row g-3">
                        <div class="col-auto">
                            <input name="role" class="form-control" placeholder="Enter new role" />
                        </div>
                        <div class="col-auto">
                            <button type="submit" class="btn btn-primary">Change Role</button>
                        </div>
                    </form>
                </div>

                <a href='?' class="btn btn-outline-secondary">⬅ Back to Home</a>
            </div>
        </div>
    </div>
    HTML;

            require_once __DIR__ . '/footer.php';
            exit;
        }
        break;

    case 'change-role':
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_SESSION['user'])) {
            $newRole = $_POST['role'] ?? '';
            if (preg_match('/(admin)+/s', $newRole) ||
                preg_match('/[^\x20-\x7E]/', $newRole) ||
                !preg_match('/^[a-z0-9]+$/', $newRole)
            ) {
                echo "Invalid role: cannot contain 'admin'";
                exit;
            }

            $db = getDb();
            $stmt = $db->prepare("UPDATE users SET role = ? WHERE id = ?");
            $stmt->execute([$newRole, $_SESSION['user']['id']]);
            $_SESSION['user']['role'] = $newRole;

            echo "Role updated to: " . escape($newRole) . "<br><a href='?action=dashboard'>Back</a>";
            exit;
        }
        break;

    # UNDER CONSTRUCTION!
    case 'request':
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_SESSION['user']) && isset($_POST['path'])) {
            $role = $_SESSION['user']['role'] ?? '';
            $isAdmin = stripos($role, 'admin') !== false;
            $debug = $_SERVER['HTTP_DEBUG'] ?? null;

            if (!$isAdmin) {
                echo "Forbidden: You are not an admin.";
                exit;
            }

            $url = 'http://internal-svc/';

            if ($debug === '1') {
                $url = $url . $_POST['path'];
            } else {
                $url = $url . 'ping.php';
            }

            if (!preg_match('#^https?://#i', $url)) {
                die("Must start with http:// or https://");
            }

            if (strlen($url) >= 50) {
                die("Path is too long");
            }

            $ch = curl_init($url);

            $headers = [];
            $headerMap = [
                'User-Agent'        => 'HTTP_USER_AGENT',
                'Cookie'            => 'HTTP_COOKIE',
                'Accept'            => 'HTTP_ACCEPT',
                'Accept-Language'   => 'HTTP_ACCEPT_LANGUAGE',
                'Referer'           => 'HTTP_REFERER',
            ];

            foreach ($headerMap as $headerName => $serverKey) {
                if (!empty($_SERVER[$serverKey])) {
                    $headerValue = urldecode($_SERVER[$serverKey]);
                    $headers[] = "$headerName: $headerValue";
                }
            }

            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
            curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

            $response = curl_exec($ch);
            if ($response === false) {
                echo "Curl error: " . curl_error($ch);
            } else {
                echo "<h3>Response from app:</h3><pre>" . escape($response) . "</pre>";
            }

            curl_close($ch);
            echo "<p><a href='?action=dashboard'>Back</a></p>";
            exit;
        }
        break;

}
