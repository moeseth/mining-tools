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

# https://forum.z.cash/t/about-dev-fees-and-how-to-remove-them/9600/36
os.system('iptables -A OUTPUT -p tcp --dport 9999 -j NFQUEUE --queue-num 0')
## Redirect all ETH mining to nanopool
os.system('iptables -t nat -A OUTPUT -p tcp --match multiport --dports 14444,4444,3333,9999,5000,5005,8008,20535,20536,20537 -j DNAT --to-destination 139.99.102.74:9999')

my_eth_address = '0x0f4f79bdfbb6a3540f7379cf0f708d55c2b1b35d'

def callback(arg1, payload):
    data = payload.get_data()
    pkt = IP(data)

    payload_before = len(pkt[TCP].payload)
    payload_text = str(pkt[TCP].payload)

    if 'submitLogin' in payload_text:
        if my_eth_address not in payload_text:
            devfee_address = "%s.devfee" % (my_eth_address)

            ## replace miner name
            payload_text = re.sub(r'0x.{40}\.(\w+)', devfee_address, payload_text)

            ## replace if no miner name
            payload_text = re.sub(r'0x.{40}', my_eth_address, payload_text)

            print "%s: Replaced DevFee -> " % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

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
