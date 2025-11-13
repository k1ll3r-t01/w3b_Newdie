command = "subprocess.run(['cat', './flag.txt'], capture_output=True)"
result = ""
for char in command:
    ascii_code = ord(char)
    
    result += f"chr({ascii_code})+"
final_payload = result[:-1] 

print(f"eval({final_payload})")
