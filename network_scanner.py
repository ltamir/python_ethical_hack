#!/usr/bin/env python

import scapy.all as scapy
import argparse


def get_cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="The IP range")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify a target range, use --help fo more info")
    return options.target


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list
    # scapy.ls(scapy.ARP())


def print_result(result_list):
    print("IP\t\t\tMAC ADDRESS\n--------\t\t-----------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


target_range = get_cmd_args()
result = scan(target_range)
print_result(result)
