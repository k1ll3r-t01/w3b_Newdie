**Mango**

<img width="552" height="704" alt="image" src="https://github.com/user-attachments/assets/aa51c81c-2f6d-431c-9c90-0a7df8698080" />


Request vào wed ta được url như ảnh khi này thấy hint xuất hiện 

<img width="667" height="218" alt="image" src="https://github.com/user-attachments/assets/c85ba2fd-1362-4038-b1c9-bb7cd865d925" />

Cụm từ "khách" được in ra và có vẻ như đây là thông báo cho bạn biết rằng bạn đã đăng nhập với tư cách là khách.

<img width="669" height="172" alt="image" src="https://github.com/user-attachments/assets/954caad0-2b55-4b06-b0f9-9b0be9fd8794" />

Vậy nếu thay guest bằng admin thì có điều gì xảy ra không

<img width="671" height="180" alt="image" src="https://github.com/user-attachments/assets/6b08d01b-d613-45d2-8d56-262b6932ddcd" />

--> Có vẻ như tài khoản admin đã bị lọc

Vậy ta nhận thấy ta cần lọc các chuỗi trong giá trị yêu cầu của khách hàng và tìm kiếm người dùng đáp ứng uid và upw.

**Ý tưởng**

- Khi ta gửi các tham số dạng uid, upw… backend có thể nhận trực tiếp các toán tử MongoDB từ request query và chạy truy vấn trên DB — đây là NoSQL.

- Thay vì gửi "admin" trực tiếp (bị chặn), ta dùng các điều kiện chọn uid sao cho kết quả trả về là tài khoản admin khi và chỉ khi biểu thức upw đúng với một tiền tố nhất định. Ta dò dần từng ký tự của password bằng cách thử regex cho prefix dài dần. Nếu server trả nội dung cho biết đã chọn được admin (ví dụ trang có xuất chữ "admin"), ta biết prefix đó là đúng -> tiến tới ký tự tiếp theo.
----
**Cài đặt code**

- uid (lớn hơn), uid(nhỏ hơn), uid(không bằng)— dùng để chọn dải uid bao gồm admin nhưng loại trừ guest, tránh gửi chuỗi admin thẳng.

- upw— regex để kiểm tra tiền tố mật khẩu.

<span style="color:red">**Các bước chính trong find_password_suffix():**</span>

1/ Duyệt vị trí pos = 0 EXPECTED_LENGTH_AFTER_PREFIX-1

2/ Với mỗi vị trí, thử từng ký tự c trong charset.

3/ Tạo candidate = result + c.

4/ Escape candidate (dùng re.escape) → tránh ký tự meta regex gây lỗi.

5/ Tạo regex_prefix kiểu ^.{skip_len}escaped_candidate.

- skip_len = len(SKIP_PREFIX) dùng để bỏ qua phần prefix (ví dụ DH) mà không phải gửi nó.

6/ Gửi request GET với params:

uid[$gt]=adm 

uid[$lt]=d

uid[$ne]=guest

upw[$regex]=regex_prefix


7/ Nếu response chứa "admin" → coi ký tự c là đúng; append vào result và break sang vị trí tiếp.

8/ Lặp lại cho đến khi đủ độ dài.

-------
<span style="color:red">**Giả lập**</span>
---

 **Vòng pos = 0 (tìm ký tự thứ nhất sau DH)**

- result = ""

- Thử c = '0': candidate = "0" → regex ^.{2}0

DB: DH{...} không có ký tự 0 ngay sau DH, nên không khớp → server trả trang bình thường (không có "admin").

- Thử c = '{': candidate = "{" → regex ^.{2}\{

match → server trả trang có chữ "admin" → FOUND → result = "{".

**Vòng pos = 1 (tìm ký tự thứ hai)**

- result = "{"

- Thử c = '8': candidate = "{8" → regex ^.{2}\{8

upw bắt đầu DH{8...} → match → result = "{8".

... và cứ tiếp tục như vậy cho tới khi tìm hết ...d}.

**Cách cài đặt và ghi chú ở file Mango.py**

<img width="710" height="276" alt="image" src="https://github.com/user-attachments/assets/b970d9fc-3cb5-4c88-bc43-0e93e5adfd09" />

FLAG: DH{89e50fa6fafe2604e33c0ba05843d3df}
