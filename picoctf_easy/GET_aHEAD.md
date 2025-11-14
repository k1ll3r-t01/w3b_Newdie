## Challenge: GET aHEAD
### Information
<img src="https://github.com/user-attachments/files/23537891/0.md" width="500">

### Hints
1. Maybe you have more than 2 choices
2. Check out tools like Burpsuite to modify your requests and look at the responses
### Solution
Vào Burp Suite -> Open Browser -> Dán link từ đề bài  
<img src="https://github.com/user-attachments/files/23537843/2.md" width="900">

Bật **Intercept** và nhấn **Choose Red**, Burp Suite bắt được `HTTP GET` như sau
```http
GET /index.php? HTTP/1.1
Host: mercury.picoctf.net:53554
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://mercury.picoctf.net:53554/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```
Vì đề bài là **GET aHEAD**, ta chọn **Send to Repeater**, sửa Request từ `GET` thành `HEAD`  
Bấm **Send** và ta có được flag  
<img src="https://github.com/user-attachments/files/23537888/1.md" width="900">

