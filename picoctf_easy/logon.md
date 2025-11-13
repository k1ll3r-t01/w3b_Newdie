## Challenge: logon
### Information
![image][]
### Hint
Hmm it doesn't seem to check anyone's password, except for Joe's?
### Solution
Ta nhập thử `Username: joe` và `Password: 12345`, khi Sign in sẽ nhận được  
Mở DevTools và check phần Application, ta thấy hiển thị các dòng như sau:  
Sửa giá trị của `admin` thì `False` thành `True` và reload lại trang web ta nhận được flag
