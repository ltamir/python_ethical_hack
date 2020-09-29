#!/usr/bin/python2

import requests
from BeautifulSoup import BeautifulSoup
import urlparse

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "http://10.0.2.15/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)
dataDict = {}

parsed_html = BeautifulSoup(response.content)
forms_list = parsed_html.findAll("form")

for form in forms_list:
    
    post_url = urlparse.urljoin(target_url, form.get("action"))
    print("method=" + form.get("method"))

    inputs_list = form.findAll("input")
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("type")
        if input_type == "text":
            input_value="test"
        dataDict[input_name] = input_value
    result = requests.post(post_url, data = dataDict)
    print(result.content)
        