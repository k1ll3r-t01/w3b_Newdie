## WEB-SSRF 
This is an image viewer service written in Flask. Use SSRF vulnerabilities to obtain flags. The flag is /app/flag.txt located at.
<img width="1086" height="374" alt="image" src="https://github.com/user-attachments/assets/284dd3d5-d6da-4c3c-b148-1385deeb989d" />

<img width="2766" height="1502" alt="image" src="https://github.com/user-attachments/assets/aaae4eb9-9948-4fb3-ac16-b9a556ea16e8" />
Nhập thử /app/flag.txt
Ta vào check source gốc thì chỉ thấy một dòng dài chứa mã encode base64
<img width="2706" height="172" alt="image" src="https://github.com/user-attachments/assets/0c46ad63-5f4a-4ce7-8de1-32c8956ca208" />

`PCFkb2N0eXBlIGh0bWw+CjxodG1sIGxhbmc9ZW4+Cjx0aXRsZT40MDQgTm90IEZvdW5kPC90aXRsZT4KPGgxPk5vdCBGb3VuZDwvaDE+CjxwPlRoZSByZXF1ZXN0ZWQgVVJMIHdhcyBub3QgZm91bmQgb24gdGhlIHNlcnZlci4gSWYgeW91IGVudGVyZWQgdGhlIFVSTCBtYW51YWxseSBwbGVhc2UgY2hlY2sgeW91ciBzcGVsbGluZyBhbmQgdHJ5IGFnYWluLjwvcD4K `
Mã hóa từ base 64 ta được:
```
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
```
