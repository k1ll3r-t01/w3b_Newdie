# `weblog-1`
## Solution
### 1.

Khi truy cập vào trang web challenge, ta thấy giao diện có chỗ cho phép nhập tham số `sort`.
Ta thử nhập 1 giá trị bất kỳ, và quan sát web trả về:

Trang web ghép trực tiếp nội dung ta nhập vào câu lệnh SQL và hiển thị công khai câu query phía dưới.
> #### VD:
> ```SELECT username FROM board ORDER BY {INPUT}```

Điều này cho thấy tham số này`không được lọc`, và ta có thể chèn payload vào.

> → Đây chính là một lỗ hổng SQL Injection dạng `Blind-SQL` dựa trên độ dài phản hồi.

Từ log của server, ta thấy khi truy vấn đúng → độ dài `response = 1192`, sai → `841`.
Nhờ đó ta có thể biết điều kiện đúng/sai dù không thấy kết quả query.

### 2.

Dựa vào log mà ta phân tích từ file challenge:

Hacker đang khai thác trường `sort` để dò từng ký tự của thông tin nhạy cảm.

Dãy kết quả họ truy ra được (dưới dạng ASCII) là:
```acsii
97,100,109,105,110,58,84,104,49,115,95,49,115,95,65,100,109,49,110,95,80,64,83,83,44,103,117,101,115,116,58,103,117,101,115,116
```
Chuyển đổi `ASCII → chuỗi`:
```
admin:Th1s_1s_Adm1n_P@SS,guest:guest
```
Như vậy ta biết:

- Bảng chứa thông tin: `users`

- Username: `admin`

- Password: `Th1s_1s_Adm1n_P@SS`

Ngoài ra còn có user `guest` nhưng không quan trọng.

Đây là “flag” trong bài viết gốc, vì nhiệm vụ bài là phân tích log để khôi phục thông tin mà attacker đã tìm ra.

### 3.

Sau khi có được tài khoản admin, hacker chuyển sang khai thác lỗi `LFI (Local File Inclusion)` trong đường dẫn:
```bash
/admin/?page=php://filter/convert.base64-encode/resource=../config.php
```
Payload này sử dụng `php://filter` để đọc file `config.php` dưới dạng `base64`.

Trong log ta thấy rõ truy vấn này → chứng tỏ `LFI` hoạt động thành công.


### 4.

Tiếp theo, attacker khai thác thêm 1 lỗ hổng khác:

Trong file `/admin/memo.php`, giá trị `memo` do user nhập được lưu vào:
```
$_SESSION["memo"]
```
Sau đó session này lưu thành file trong thư mục:
```
/var/lib/php/sessions/sess_<ID>
```
Attacker đã ghi mã `PHP` vào trường `memo` → và đọc lại file session qua `LFI`.

Session chứa code:
```php
function m($l,$T=0){
  $K = date('Y-m-d');
  ...
  return $l;
}
echo m('bmha[tqp[...]');
```
Mã này bị obfuscate, nhưng dựa vào log server ta biết thời điểm tấn công:
→ ngày `2020-06-02`

Khi thay `date('Y-m-d')` bằng `'2020-06-02'` và decode, ta thu được:

→ Webshell được lưu tại:
```css
/var/www/html/uploads/images.php
```

Trong log còn có truy vấn:
```bash

GET /uploads/images.php?c=whoami
```
> → Chứng tỏ webshell đã được sử dụng để thực thi lệnh.
