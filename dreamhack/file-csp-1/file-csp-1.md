## file-csp-1
---

# 🛡️ **Writeup – CSP Challenge (Dreamhack)**

Challenge cung cấp 3 route chính:

* `/test` – thử payload CSP tùy ý
* `/live` – trang thật để kiểm tra hiệu ứng CSP
* `/verify` – route mà bot (Chromedriver) sẽ load để đánh giá CSP ta gửi → qua được thì nhận flag

---

# 🔍 1. **Phân tích code tại `/verify`**

Code `/verify` hoạt động như sau:

```python
driver.get(f'http://localhost:8000/live?csp={quote(csp)}')
```

→ Ta gửi CSP vào form POST, và bot sẽ load `/live` với tham số `?csp=` chứa policy của ta.

Sau đó bot chạy 4 script:

```python
a = driver.execute_script('return a()')
b = driver.execute_script('return b()')
c = driver.execute_script('return c()')
d = driver.execute_script('return $(document)')
```

Để lấy flag, điều kiện bắt buộc:

```
a == 'error'
b == 'error'
c == 'c'
d != 'error'
```

Nghĩa là:

| Script | Yêu cầu                         |
| ------ | ------------------------------- |
| `a()`  | PHẢI lỗi → script phải bị block |
| `b()`  | PHẢI lỗi → script phải bị block |
| `c()`  | PHẢI chạy → script được phép    |
| jQuery | PHẢI chạy → jquery được phép    |

---

# 🧪 2. **Phân tích nội dung trong `/live` (csp.html)**

Trang `/live` chứa:

```html
<!-- block me -->
<script>
    function a() { return 'a'; }
</script>

<!-- block me -->
<script nonce="i_am_super_random">
    function b() { return 'b'; }
</script>

<!-- allow me -->
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js"
 integrity="sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8="
 crossorigin="anonymous"></script>

<!-- allow me -->
<script nonce="i_am_super_random">
    function c() { return 'c'; }
</script>
```

Yêu cầu:

| Script   | Nội dung                         | Trạng thái |
| -------- | -------------------------------- | ---------- |
| Script 1 | Inline không nonce               | ❌ Block    |
| Script 2 | Inline nonce="i_am_super_random" | ❌ Block    |
| Script 3 | jQuery CDN + integrity           | ✅ Allow    |
| Script 4 | Inline nonce="i_am_super_random" | ✅ Allow    |

---

# 🎯 3. **Vấn đề chính**

Script 2 **và** Script 4 đều dùng **cùng một nonce**:

```
nonce="i_am_super_random"
```

Nhưng ta phải:

* Block script thứ 2
* Allow script thứ 4

→ Điều này *không thể làm được bằng nonce*, vì cùng nonce = cùng quyền.

---

# 💡 4. **Ý tưởng bypass**

Dùng **hash-based CSP**:
Chỉ cho phép script dựa trên **SHA256 hash**, không phải dựa vào nonce.

Khi ta đặt:

```
script-src 'sha256-...'
```

→ Chỉ script nào khớp hash mới chạy.

Ta có jQuery sử dụng integrity:

```
sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8=
```

→ CSP cũng chấp nhận hash này.

Khi ta thử payload trong `/test`:

```
script-src 'sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8='
```

Kết quả:

* Script 1: ❌ Block (không nonce, không hash)
* Script 2: ❌ Block (hash sai)
* Script 3: ✅ Allow (hash đúng)
* Script 4: ❌ Block (inline, hash không khớp)

→ Vấn đề: **Script 4 bị block**, nhưng ta cần phải allow nó (để c() chạy).

---

# ✨ 5. **Giải pháp cuối cùng**

→ Tính hash SHA256 của script thứ 4 để allow nó.

Script thứ 4 là:

```js
function c() {
    return 'c';
}
document.write('c: allow me!<br>');
try {
    $(document);
    document.write('jquery: allow me!<br>');
} catch (e) {}
```

Giải pháp:

1. Copy nội dung script 4
2. Tính SHA256 base64
3. Cho phép hash này trong CSP
Tool: https://centralcsp.com/features/hashes
→ Từ writeup gốc và các thử đề, hash của script thứ 4 là:

```
sha256-l1OSKODPRVBa1/91J7WfPisrJ6WCxCRnKFzXaOkpsY4=
```

Do đó CSP hoàn chỉnh:

```
script-src 'sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8=' 'sha256-l1OSKODPRVBa1/91J7WfPisrJ6WCxCRnKFzXaOkpsY4=';
```

---

# 🏁 6. **Submit CSP vào `/verify`**

Gửi CSP:

```
script-src 'sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8=' 'sha256-l1OSKODPRVBa1/91J7WfPisrJ6WCxCRnKFzXaOkpsY4=';
```

Bot sẽ:

* Block script a() → OK
* Block script b() → OK
* Allow jQuery → OK
* Allow script c() → OK

Điều kiện khớp → **trả flag**.
<img width="1044" height="550" alt="image" src="https://github.com/user-attachments/assets/5d3a52b9-4113-4b5a-a840-d80041731fe8" />
Flag:
DH{csp-is-good_XD}


