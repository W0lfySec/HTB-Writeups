## --------->> BlackHole <<----------

// when extract Blackhole.zip we get archive.zip

// lets uzip him too

    $ unzip archive.zip 
    Archive:  archive.zip
      inflating: hawking                 

// extracted file called 'hawking'

    $ ls
    Blackhole.zip  archive.zip  hawking

// Lets check wich file is it

    $ file hawking 
    hawking: JPEG image data, JFIF standard 1.01, aspect ratio, density 72x72, segment length 16, baseline, precision 8, 794x579, components 3

// seems to be a picture(.jpeg)

// we will add .jpeg to image

    $ cp hawking hawking1.jpeg

// open the image hawking.jpeg

![Imnage 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/BlackHole/1.png)

// The photo gets us nowhere...

// lets check if there is some hiden files inside the picture with steghide toole

    $ steghide extract -sf hawking 
    Enter passphrase: 
    wrote extracted data to "flag.txt".

// indeed there's hidden file called 'flag.txt'

    $ ls
    Blackhole.zip  archive.zip  flag.txt  hawking


    $ cat flag.txt 

    UldaeFluUnhlaUJKZFhoNGRXMTVJRlJ0YVhkMWVuTWdhVzFsSUcxNklGRjZjM2gxWlhRZ1puUnhZV1J4Wm5WdmJYZ2dZblJyWlhWdmRXVm1MQ0J2WVdWNVlYaGhjM1ZsWml3Z2JYcHdJRzFuWm5SaFpDd2dhWFJoSUdsdFpTQndkV1J4YjJaaFpDQmhjaUJrY1dWeGJXUnZkQ0J0WmlCbWRIRWdUM0Y2Wm1SeElISmhaQ0JHZEhGaFpIRm1kVzl0ZUNCUFlXVjVZWGhoYzJzZ2JXWWdablJ4SUVkNmRXaHhaR1YxWm1zZ1lYSWdUMjE1Ym1SMWNITnhJRzFtSUdaMGNTQm1kWGx4SUdGeUlIUjFaU0J3Y1cxbWRDNGdWSEVnYVcxbElHWjBjU0JZWjI5dFpYVnRlaUJDWkdGeWNXVmxZV1FnWVhJZ1dXMW1kSEY1YldaMWIyVWdiV1lnWm5SeElFZDZkV2h4WkdWMVptc2dZWElnVDIxNWJtUjFjSE54SUc1eFptbHhjWG9nTVRrM09TQnRlbkFnTWpBd09TNGdWRzFwZDNWNmN5QnRiM1IxY1doeGNDQnZZWGw1Y1dSdmRXMTRJR1ZuYjI5eFpXVWdhWFZtZENCbGNXaHhaRzE0SUdsaFpIZGxJR0Z5SUdKaFltZDRiV1FnWlc5MWNYcHZjU0IxZWlCcGRIVnZkQ0IwY1NCd2RXVnZaMlZsY1dVZ2RIVmxJR0ZwZWlCbWRIRmhaSFZ4WlNCdGVuQWdiMkZsZVdGNFlYTnJJSFY2SUhOeGVuRmtiWGd1SUZSMVpTQnVZV0YzSUUwZ1RtUjFjWElnVkhWbFptRmtheUJoY2lCR2RYbHhJRzFpWW5GdFpIRndJR0Y2SUdaMGNTQk9aSFZtZFdWMElFVm5lbkJ0YXlCR2RYbHhaU0J1Y1dWbUxXVnhlSGh4WkNCNGRXVm1JSEpoWkNCdElHUnhiMkZrY0MxdVpIRnRkM1Y2Y3lBeU16Y2dhWEZ4ZDJVdUlGUnRhWGQxZW5NZ2FXMWxJRzBnY25GNGVHRnBJR0Z5SUdaMGNTQkVZV3R0ZUNCRllXOTFjV1pyTENCdElIaDFjbkZtZFhseElIbHhlVzV4WkNCaGNpQm1kSEVnUW1GNlpuVnlkVzl0ZUNCTmIyMXdjWGxySUdGeUlFVnZkWEY2YjNGbExDQnRlbkFnYlNCa2NXOTFZblZ4ZW1ZZ1lYSWdablJ4SUVKa2NXVjFjSEY2Wm5WdGVDQlpjWEJ0ZUNCaGNpQlNaSEZ4Y0dGNUxDQm1kSEVnZEhWemRIRmxaaUJ2ZFdoMWVIVnRlaUJ0YVcxa2NDQjFlaUJtZEhFZ1IzcDFabkZ3SUVWbWJXWnhaUzRnVlhvZ01qQXdNaXdnVkcxcGQzVjZjeUJwYldVZ1pHMTZkM0Z3SUhwbmVXNXhaQ0F5TlNCMWVpQm1kSEVnVGs1UFhPS0FtV1VnWW1GNGVDQmhjaUJtZEhFZ01UQXdJRk5rY1cxbWNXVm1JRTVrZFdaaGVtVXVEUXBVUms1N1dqTm9jVVJmZUROR1gyWlVNMTl1TkdWR2JVUndOVjlUTTJaZlN6Qm5YM0F3YVZwOUlBPT0=

// its seems to be some encrypted data

// we will decrypt it using online tool CyberChef https://gchq.github.io/CyberChef/

// // >> cybercheff recipe >> from Base64 >> from Base64 >> ROT13 (Amount:14)

![Imnage 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/BlackHole/2.png)

// Output:
Stephen William Hawking was an English theoretical physicist, cosmologist, and author, who was director of research at the Centre for Theoretical
Cosmology at the University of Cambridge at the time of his death. He was the Lucasian Professor of Mathematics at the University of Cambridge
between 1979 and 2009. Hawking achieved commercial success with several works of popular science in which he discusses his own theories and cosmology
in general. His book A Brief History of Time appeared on the British Sunday Times best-seller list for a record-breaking 237 weeks.
Hawking was a fellow of the Royal Society, a lifetime member of the Pontifical Academy of Sciences, and a recipient of the Presidential Medal of Freedom,
the highest civilian award in the United States. In 2002, Hawking was ranked number 25 in the BBC\’s poll of the 100 Greatest Britons.
HTB{N3veR_l3T_tH3_b4sTaRd5_G3t_Y0u_d0wN} 

// flag:

HTB{N3veR_l3T_tH3_b4sTaRd5_G3t_Y0u_d0wN} 
