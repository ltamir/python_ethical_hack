#!/usr/bin/python2

import requests


target_url = "http://10.0.2.15/dvwa/login.php"

formData = {"username" : "admin", "password":"password", "Login":"submit"}
response = requests.post(target_url, data=formData)
print(response.content)