#!/usr/bin/python2

import requests

target_url = "10.0.2.15/mutillidae"

def request(url):
    try:
        return requests.get("http://" + url, timeout=7)
    except requests.exceptions.ConnectionError:
        pass

with open("./common.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] url --> " + test_url)
