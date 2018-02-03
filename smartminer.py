#!/usr/bin/env python

## figure out the most profitable coin and switch automatically to mine that coin
## if you are using, will need to change miner path

import requests
import json
import os
import re
import subprocess

def check_process(process):
    returnprocess = False
    s = subprocess.Popen(["ps", "aux"],stdout=subprocess.PIPE)

    text = s.stdout.read()
    return re.search(process, text)


url = "http://whattomine.com/coins.json"

response = requests.get(url)
json_obj = json.loads(response.text)
coins = json_obj["coins"]

profitability = {}
for coin in coins:
    coin_info = coins[coin]
    lagging = coin_info["lagging"]
    algorithm = coin_info["algorithm"]

    if coin != "Nicehash-Ethash" and not lagging:
        if algorithm == 'CryptoNight' or algorithm == 'Ethash':
            profitability[coin] = coin_info["profitability24"]

sorted_list = sorted(profitability.iteritems(), key=lambda (k,v): (v,k), reverse=True)

best_coin = sorted_list[0]
coin_name = best_coin[0]
if coin_name in ("Pirl", "Ellaism", "Ethereum", "Electroneum"):
    process_name = "pirl"
    if coin_name == "Ellaism":
        process_name = "ella"
    elif coin_name == "Ethereum":
        process_name = "eth"
    elif coin_name == "Electroneum":
        process_name = "etn"

    status = check_process(process_name)

    if not status:
        print "changing miner"
        ## kill existing process
        os.system("iptables -F")
        os.system("pkill -f fee.py")
        os.system("pkill -f nsgpucnminer")
        os.system("pkill -f ethdcrminer64")
        os.system("systemctl stop ether")

        if coin_name == "Pirl":
            os.system("nohup bash /home/moe/Desktop/claymore_ether/start_pirl.bash &")
        elif coin_info == "Ellaism":
            os.system("nohup bash /home/moe/Desktop/claymore_ether/start_ella.bash &")
        elif coin_info == "Ethereum":
            os.system("nohup bash /home/moe/Desktop/claymore_ether/start.bash &")
        elif coin_info == "Electroneum":
            os.system("nohup sh /home/moe/Desktop/cryptonote/start_etn.sh &")
    else:
        print "already running"
