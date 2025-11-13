## Challenge: logon
### Information
<img width="500" src="https://github.com/user-attachments/assets/ca2f1335-2b8a-4610-89c9-5937ca705fb2" />

### Hint
Hmm it doesn't seem to check anyone's password, except for Joe's?
### Solution
<img width="700" src="https://github.com/user-attachments/assets/b4e82209-c6cb-4f88-ba8d-c99759f08a6f" />
  
Ta nhập thử `Username: joe` và `Password: 12345`, khi Sign in sẽ nhận được  
<img width="700" src="https://github.com/user-attachments/assets/20cf12e4-0579-4e0c-9a25-90575610c832" />
  
Mở DevTools và check phần Application, ta thấy hiển thị các dòng như sau:  
<img width="700" src="https://github.com/user-attachments/assets/50da3a3c-11d2-4890-8062-2d5893bdcf4f" />
  
Sửa giá trị của `admin` từ `False` thành `True` và reload lại trang web ta nhận được flag
<img width="700" src="https://github.com/user-attachments/assets/8b4e4d7b-ccbc-4798-b73c-fedd3973267c" />
