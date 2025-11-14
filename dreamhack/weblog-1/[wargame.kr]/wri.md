# `[wargame.kr] md5 password`
## Solution
### 1. Phân tích mã nguồn
Mã nguồn của bài cho thấy dù đã dùng `mysqli_real_escape_string` để lọc input `ps`, nhưng code lại chèn `md5($ps, true)` vào câu truy vấn SQL:
```sql
select * from admin_password where password='".md5($ps, true)."'
```
Tham số `true` khiến hàm `md5()` trả về 16 bytes nhị phân thô, không phải chuỗi hex 32 ký tự. Điều này cho phép chúng ta tạo ra một payload `SQL Injection` sau khi hash, vượt qua bộ lọc.


## 2. Phương pháp khai thác (Magic Hash)
Mục tiêu là tìm một chuỗi     `ps` sao cho 16 bytes thô của hash chứa chuỗi `b"'='"`.

Nếu hash trả về có dạng `[bytes]'='[bytes]`, câu truy vấn sẽ trở thành:
```sql
... where password='[bytes]'='[bytes]'
```
MySQL sẽ hiểu đây là (password = '[bytes]') = '[bytes]'.

- Vế (password = '[bytes]') gần như luôn sai, trả về 0 (false).

- Câu lệnh trở thành where 0 = '[bytes]'.

- Do "Type Juggling", MySQL ép kiểu chuỗi [bytes] (nếu không bắt đầu bằng số) thành 0.

- Câu lệnh cuối cùng là where 0 = 0, luôn TRUE và trả về Flag.
## 3. Tìm Payload
Ta dùng script Python sau để brute-force tìm một số `i` sao cho `md5(i)` chứa `b"'='"`:
```python
import hashlib

for i in range(100000000):
    raw_hash = hashlib.md5(str(i).encode()).digest()
    
    if b"'='" in raw_hash:
        print(f"Giá trị (ps): {i}")
        print(f"Hash (bytes): {raw_hash}")
        break
```
## 4. Lấy Flag
Script sẽ tìm thấy giá trị "magic" là: `240610708`.

Chỉ cần nhập `240610708` vào ô mật khẩu và submit để lấy Flag.
