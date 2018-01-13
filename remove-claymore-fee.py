# based on:
# https://stackoverflow.com/questions/27293924/change-tcp-payload-with-nfqueue-scapy?rq=1
# https://github.com/DanMcInerney/cookiejack/blob/master/cookiejack.py

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import nfqueue
from scapy.all import *
import os
import re
from os import path
from datetime import datetime, timedelta
import json
from collections import OrderedDict

# https://forum.z.cash/t/about-dev-fees-and-how-to-remove-them/9600/36
os.system('iptables -A OUTPUT -p tcp --dport 4444 -j NFQUEUE --queue-num 0')  # for dwarfpool
#os.system('iptables -A OUTPUT -p tcp --dport 9999 -d eth-us-west1.nanopool.org -j NFQUEUE --queue-num 0')
#os.system('iptables -A OUTPUT -p tcp --dport 5000 -j NFQUEUE --queue-num 0')
#os.system('iptables -A INPUT -p tcp --dport 5000 -j NFQUEUE --queue-num 0')

my_eth_address = '0x0f4f79bdfbb6a3540f7379cf0f708d55c2b1b35d'

def callback(arg1, payload):
  data = payload.get_data()
  pkt = IP(data)

  payload_before = len(pkt[TCP].payload)

  payload_text = str(pkt[TCP].payload)
  # jason
##  print("%s:%s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), payload_text))
  if ('submitLogin' in payload_text) or ('eth_login' in payload_text):
    json_data=json.loads(payload_text, object_pairs_hook=OrderedDict)
    if json_data['params']:
      if my_eth_address not in json_data['params'][0]:
        print('[*] DevFee Detected - Replacing Address - %s\n' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('[*] REPLACED FROM %s TO %s\n' % (json_data['params'][0], my_eth_address))
        json_data['params'][0] = "%s.devfee" % (my_eth_address)
        print("[*] BEFORE: %s\n" % payload_text)
        print("[*] AFTER: %s\n" % json.dumps(json_data))
        payload_text=json.dumps(json_data) + '\n'
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
