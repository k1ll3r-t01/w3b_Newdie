## Challenge: Includes
### Information
<img src="https://github.com/user-attachments/files/23538126/0.md" width="500">

### Hint
Is there more code than what the inspector initially shows?
### Solution
View page source, ta thấy trong code HTML không có gì đặc biệt
```html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="style.css">
    <title>On Includes</title>
  </head>
  <body>
    <script src="script.js"></script>
  
    <h1>On Includes</h1>
    <p>Many programming languages and other computer files have a directive, 
       often called include (sometimes copy or import), that causes the 
       contents of a second file to be inserted into the original file. These 
       included files are called copybooks or header files. They are often used
       to define the physical layout of program data, pieces of procedural code
       and/or forward declarations while promoting encapsulation and the reuse
       of code.</p>
    <br>
    <p> Source: Wikipedia on Include directive </p>
    <button type="button" onclick="greetings();">Say hello</button>
  </body>
</html>
```

Tuy nhiên, có hai file cần lưu ý ở đây là `style.css` và `script.js`.  
Ta thử check file `style.css` và có được phần đầu tiên của flag
```css
body {
  background-color: lightblue;
}

/*  picoCTF{1nclu51v17y_1of2_  */
```

Check tiếp file `script.js` và ta có được phần còn lại của flag
```js



function greetings()
{
  alert("This code is in a separate file!");
}

//  f7w_2of2_6edef411}
```
