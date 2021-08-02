import hashlib


def ck_password():
    password = "62def4866937f08cc13bab43bb14e6f7"
    output = ""
    wordlist = "/usr/share/wordlists/rockyou.txt"
    salt = "5a599ef579066807"
    dictionar = open(wordlist)
    for line in dictionar.readlines():
        line = line.replace("\n", "")
        if hashlib.md5(str(salt) + line).hexdigest() == password:
            output += "\n[+] Password cracked: " + line
            break
    print(output)


ck_password()
