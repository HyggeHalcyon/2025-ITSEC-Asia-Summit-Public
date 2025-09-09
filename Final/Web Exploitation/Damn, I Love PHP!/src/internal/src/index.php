<?php
    error_reporting(0);
    $digit = $_GET['digit'];
    if ((int) $digit) {
        $forbiddenChars = array('\\', '<', '>', '`', '~', '(' , ')', ',', '+', '-', '/', '*', '^', '|', '&', '!', '?', ':', ';', '.');

        foreach ($forbiddenChars as $char) {
            if (strpos($digit, $char) !== false) {
                http_response_code(403);
                die('403 Forbidden');
            }
        }
    } else {
        $digit = "0";
    }

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Internal Calculator</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <h1>Internal Calculator</h1>
    <h3 class="result"></h3>
    <form action="/">
        <input type="text" name="digit" placeholder="Enter a digit">
        <input type="submit" value="Calculate">
    </form>
    <script>
        var multiply = function(a, b) {
            return a * b;
        }

        var result = multiply(7, <?php echo $digit; ?>);

        document.querySelector('.result').textContent = 'The result is: ' + result;
    </script>
</body>
</html>