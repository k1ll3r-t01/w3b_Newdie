## Challenge: Bookmarklet
### Information
<img src="https://github.com/user-attachments/files/23538681/0.md" width="500">

### Hints
1. A bookmarklet is a bookmark that runs JavaScript instead of loading a webpage.
2. What happens when you click a bookmarklet?
3. Web browsers have other ways to run JavaScript too.
### Solution
<img src="https://github.com/user-attachments/files/23538709/1.md" width="900">

Ta có code JS từ text box
```js
        javascript:(function() {
            var encryptedFlag = "àÒÆÞ¦È¬ëÙ£ÖÓÚåÛÑ¢ÕÓ¡ÒÅ¤í";
            var key = "picoctf";
            var decryptedFlag = "";
            for (var i = 0; i < encryptedFlag.length; i++) {
                decryptedFlag += String.fromCharCode((encryptedFlag.charCodeAt(i) - key.charCodeAt(i % key.length) + 256) % 256);
            }
            alert(decryptedFlag);
        })();
```

Mở DevTools, vào tab Console.  
Nhập `allow pasting` để có thể paste đoạn code vừa copy vào.  
Enter và ta nhận được flag  
<img src="https://github.com/user-attachments/files/23538793/2.md" width="700">

