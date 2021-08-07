## ------------------->> 0ld is g0ld <<------------

// Extract the zipped folder, we got a pdf file that require password for open.

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Old_is_gold/1.png)

// We can crack that .pdf file password with tool called [PDFCrack](https://github.com/alitrack/PDFCrack)

    $ pdfcrack -w rockyou.txt -f 0ld\ is\ g0ld.pdf 
    
    PDF version 1.6
    Security Handler: Standard
    V: 2
    R: 3
    P: -1060
    Length: 128
    Encrypted Metadata: True
    FileID: 5c8f37d2a45eb64e9dbbf71ca3e86861
    U: 9cba5cfb1c536f1384bba7458aae3f8100000000000000000000000000000000
    O: 702cc7ced92b595274b7918dcb6dc74bedef6ef851b4b4b5b8c88732ba4dac0c
    Average Speed: 22237.5 w/s. Current Word: '252986'
    Average Speed: 22221.0 w/s. Current Word: 'ladybrandon'
    Average Speed: 22499.3 w/s. Current Word: 'kaylaxx'
    found user-password: 'jumanji69'

// We found password ! 'jumanji69'

// Open the file with passowrd we get a page with pictur

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Old_is_gold/4.png)

// rolling down we can notice something small

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Old_is_gold/5.png)

// its some symbols, lets copy that

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Old_is_gold/6.png)

    .-. .---- .--. ... .- -- ..- ...-- .-.. -- ----- .-. ... ...--

// Navigating to [CyberChef](https://gchq.github.io)

// We can decode that with recipe: 'From Morse code'

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Old_is_gold/3.png)

// And we got the flag !

    HTB{R1PSAMU3LM0RS3}
