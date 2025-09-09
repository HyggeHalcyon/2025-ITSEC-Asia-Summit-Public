<?php
session_start();

require_once __DIR__ . '/../includes/actions.php';
require_once __DIR__ . '/../includes/header.php';
?>

<div class="container mt-5">
    <div class="row">
        <!-- Register Form -->
        <div class="col-md-6 mb-4">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h3 class="card-title mb-4">Register</h3>
                    <form method="POST" action="?action=register">
                        <input class="form-control mb-3" name="username" placeholder="Username" required>
                        <input class="form-control mb-3" name="password" type="password" placeholder="Password" required>
                        <button type="submit" class="btn btn-primary w-100">Register</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Login Form -->
        <div class="col-md-6 mb-4">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h3 class="card-title mb-4">Login</h3>
                    <form method="POST" action="?action=login">
                        <input class="form-control mb-3" name="username" placeholder="Username" required>
                        <input class="form-control mb-3" name="password" type="password" placeholder="Password" required>
                        <button type="submit" class="btn btn-success w-100">Login</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<?php require_once __DIR__ . '/../includes/footer.php'; ?>
