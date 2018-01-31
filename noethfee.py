# based on:
# https://stackoverflow.com/questions/27293924/change-tcp-payload-with-nfqueue-scapy?rq=1
# https://github.com/DanMcInerney/cookiejack/blob/master/cookiejack.py

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import os
import re
import json
import nfqueue
from os import path
from scapy.all import *
from collections import OrderedDict
from datetime import datetime, timedelta

my_eth_address = '0x0f4f79bdfbb6a3540f7379cf0f708d55c2b1b35d'
## find your pool ip
pool_ip_address = '139.99.102.74'
pool_port = '9999'

# https://forum.z.cash/t/about-dev-fees-and-how-to-remove-them/9600/36
command = "iptables -A OUTPUT -p tcp --dport %s -j NFQUEUE --queue-num 0" % (pool_port)
os.system(command)

## Redirect all ETH mining to mining pool
command = "iptables -t nat -A OUTPUT -p tcp --match multiport --dports 14444,4444,3333,9999,5000,5005,8008,20535,20536,20537 -j DNAT --to-destination %s:%s" % (pool_ip_address, pool_port)
os.system(command)

def callback(arg1, payload):
    data = payload.get_data()
    pkt = IP(data)

    payload_before = len(pkt[TCP].payload)
    payload_text = str(pkt[TCP].payload)

    if 'submitLogin' in payload_text:
        if my_eth_address not in payload_text:
            payload_text = re.sub(r'0x.{40}', my_eth_address, payload_text)

            print "%s: Replaced DevFee -> %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), payload_text)

    pkt[TCP].payload = payload_text
    payload_after = len(payload_text)
    payload_dif = payload_after - payload_before
    pkt[IP].len = pkt[IP].len + payload_dif
    pkt[IP].ttl = 40

    del pkt[IP].chksum
    del pkt[TCP].chksum
    payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(pkt), len(pkt))


def main():
    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)
    q.set_callback(callback)
    q.create_queue(0)

    try:
        q.try_run() # Main loop
    except KeyboardInterrupt:
        q.unbind(socket.AF_INET)
        q.close()

    if path.exists('./restart_iptables'):
      os.system('./restart_iptables')

main()
