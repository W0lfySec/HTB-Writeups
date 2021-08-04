import hashlib


def crack_password():

    password = "62def4866937f08cc13bab43bb14e6f7"
    wordlist = "/usr/share/wordlists/rockyou.txt"
    salt = "5a599ef579066807"
    cracked = ''

    # open /usr/share/wordlists/rockyou.txt
    dictionary = open(wordlist)

    # Loop for compare hash to hash from rockyou.txt
    for line in dictionary.readlines():
    # drop down line to next passowrd
        line = line.replace("\n", "")
    # if "5a599ef579066807" + "somepassowrd" == "62def4866937f08cc13bab43bb14e6f7"
        if hashlib.md5(str(salt) + line).hexdigest() == password:
        # print cracked passowrd
            cracked += "\n[+] Password cracked: " + line
        # exit
            break
    print(cracked)


crack_password()

