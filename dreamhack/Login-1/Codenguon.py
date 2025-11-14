@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    # Nếu người dùng truy cập bằng phương thức GET -> trả về trang quên mật khẩu
    if request.method == 'GET':
        return render_template('forgot.html')

    else:
        # Lấy dữ liệu người dùng gửi từ form
        userid = request.form.get("userid")
        newpassword = request.form.get("newpassword")
        backupCode = request.form.get("backupCode", type=int)

        # Kết nối CSDL
        conn = get_db()
        cur = conn.cursor()

        # Tìm người dùng theo id
        user = cur.execute('SELECT * FROM user WHERE id = ?', (userid,)).fetchone()

        if user:

            # Chống brute-force: buộc chờ 1 giây mỗi lần thử
            time.sleep(1)

            # Nếu số lần reset vượt giới hạn MAXRESETCOUNT -> chặn
            if user['resetCount'] == MAXRESETCOUNT:
                return "<script>alert('Số lần đặt lại mật khẩu đã vượt giới hạn.');history.back(-1);</script>"

            # Nếu backupCode đúng
            if user['backupCode'] == backupCode:
                newbackupCode = makeBackupcode()

                # Cập nhật mật khẩu mới (hash SHA-256), reset backupCode, reset resetCount
                updateSQL = "UPDATE user set pw = ?, backupCode = ?, resetCount = 0 where idx = ?"
                cur.execute(updateSQL, (
                    hashlib.sha256(newpassword.encode()).hexdigest(),
                    newbackupCode,
                    str(user['idx'])
                ))

                msg = f"<b>Đổi mật khẩu thành công.</b><br/>Mã dự phòng mới: {newbackupCode}"

            else:
                # Nếu backupCode sai -> tăng số lần resetCount
                updateSQL = "UPDATE user set resetCount = resetCount+1 where idx = ?"
                cur.execute(updateSQL, (str(user['idx']),))

                msg = f"Mã dự phòng sai!<br/><b>Số lần còn lại: </b> {(MAXRESETCOUNT-1) - user['resetCount']}"

            # Lưu thay đổi vào CSDL
            conn.commit()

            # Trả về trang index với thông báo
            return render_template("index.html", msg=msg)

        # Không tìm thấy user -> báo lỗi
        return "<script>alert('Không tìm thấy người dùng.');history.back(-1);</script>"
