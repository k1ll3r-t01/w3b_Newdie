## Challenge: Crack the Gate 1
### Information
<img src="https://github.com/user-attachments/files/23536843/0.md" width="500">

### Hint
1. Developers sometimes leave notes in the code; but not always in plain text.
2. A common trick is to rotate each letter by 13 positions in the alphabet.
### Solution
View page source và tìm trong code html ta có được các dòng chú thích mà tác giả để lại
```html
 <!-- ABGR: Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf" -->
<!-- Remove before pushing to production! -->   
```

Rõ ràng đây là chuỗi ROT13, giải mã ta được `NOTE: Jack - temporary bypass: use header "X-Dev-Access: yes"`  
Điều này có nghĩa là nếu máy chủ nhận được một yêu cầu (request) có chứa HTTP Header tên là `X-Dev-Access` với giá trị là `yes`, nó sẽ cho phép đi qua.  

Dùng Burp Suite -> Proxy -> Intercept -> Open Browser -> load trang web từ đề bài và nhập email `ctf-player@picoctf.org` cùng password bất kì  
<img src="https://github.com/user-attachments/files/23537166/4.md" width="800">
  
Quay lại Burp Suite, chuyển sang trạng thái **"Intercept is on"**  
Quay lại trình duyệt, nhấn **Log in**  
Khi này, Burp Suite đã bắt được gói tin **HTTP POST**  
<img src="https://github.com/user-attachments/files/23537176/2.md" width="800">
  
Chuyển sang Repeater và nhập header `X-Dev-Access: yes`  
Sau đó bấm **Send** và ta đã có được flag  
<img src="https://github.com/user-attachments/files/23537181/3.md" width="800">
