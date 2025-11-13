## Challenge: where are the robots
### Information
<img src="https://github.com/user-attachments/files/23522094/0.md" width="500">

### Hint
What part of the website could tell you where the creator doesn't want you to look?
### Solution
Load link từ đề bài, ta thấy trang chỉ có 2 dòng, hoàn toàn không có thông tin về flag  
<img src="https://github.com/user-attachments/files/23522135/1.md" width="700">  
  
Dựa vào tên challenge và hint, ta check file robots.txt và nhận được   
```txt
User-agent: *
Disallow: /8028f.html
```
Ở đây ta đã tìm được phần "the creator doesn't want you to look"  
  
Load lại website với phần vừa tìm được và ta đã có được flag  
<img src="https://github.com/user-attachments/files/23522184/2.md" width="700">  

