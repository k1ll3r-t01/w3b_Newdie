**Crawling**
------
<img width="665" height="647" alt="image" src="https://github.com/user-attachments/assets/f2bc6500-8451-449c-8699-4c3974f2b568" />


**1.Phân tích Source**

Nhận xét:

- lookup() dùng gethostbyname() trên domain ban đầu (ví dụ shortener domain) — nên nếu domain đó là public IP, check_global(ip) trả True. 


- requests.get(url) sẽ theo redirect mặc định (requests theo redirect 3xx). Nếu shortener trả 302 → requests sẽ follow tới 127.0.0.1:3333/admin và nhận nội dung của trang admin.

- Có 1 vòng kiểm tra thêm: nếu res.text chứa chuỗi 'referer' thì code cố gắng đọc res.headers.get('refer'). Nếu admin page không chứa 'referer' thì đoạn kiểm tra không kích hoạt.

Do đó chiến lược đơn giản: đưa một URL công khai mà netloc ban đầu là public (pass check), nhưng redirect tới http://127.0.0.1:3333/admin để server ở target theo redirect và trả về nội dung admin (flag). 

<img width="514" height="413" alt="image" src="https://github.com/user-attachments/assets/3f48e3c7-7001-4756-bc05-3f20ae7553e3" />


------
**II. Tìm FLAG**

- Server chỉ kiểm tra domain ban đầu (URL người dùng nhập),
không kiểm tra URL sau redirect.

===> Do đó, nếu ta cung cấp 1 URL có domain public, nhưng redirect đến:

```bash
127.0.0.1:3333/admin
```
thì server sẽ follow → gửi request từ localhost → nhận flag.

**1.Tạo short URL để redirect nội bộ**

Dùng trang rút gọn link https://is.gd/

Nhập vào 
```bash
http://127.0.0.1:3333/admin
```
Trang trả ra link dạng:
```bash
https://lstwr.com/l165GI
```
Nhập link này vào URL ta thu được FLAG

<img width="527" height="412" alt="image" src="https://github.com/user-attachments/assets/b1275c7a-f98d-4a51-bfe0-d17a2da30c26" />

FLAG:
```bash
DH{d881f7e8ef64f32224a4db6d6764466a}
```
