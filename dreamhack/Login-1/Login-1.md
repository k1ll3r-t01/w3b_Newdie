## Login-1
Đầu tiên, đoạn mã này nhìn qua có vẻ an toàn và không dễ khai thác. Tuy nhiên, chính lệnh time.sleep(1) lại trở thành chìa khóa mở ra lỗ hổng Race Condition (điều kiện tranh chấp).

Trong hệ thống, có 100 mã dự phòng hợp lệ (từ 0 đến 100). Điều này cho phép ta thực hiện brute-force một cách hiệu quả.
Để vượt qua cơ chế giới hạn số lần đặt lại mật khẩu (resetCount), ta chỉ cần gửi 100 yêu cầu đồng thời, mỗi yêu cầu thử một mã dự phòng khác nhau. Nếu thực hiện đúng thời điểm, server sẽ xử lý nhiều yêu cầu song song trước khi kịp tăng resetCount, và như vậy ta có thể đặt lại mật khẩu thành công.

Ngoài ra, ta còn có một điểm tấn công khác: kiểm tra xem tài khoản nào đang có quyền quản trị qua endpoint /user/<int:useridx>.
Khi truy cập thử /user/14, tôi phát hiện ra người dùng orange đang sở hữu quyền admin.
