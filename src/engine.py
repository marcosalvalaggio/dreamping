from icmplib import ping
import datetime
from typing import List
import time
import subprocess
import re
import requests

def check_host(host: str, name: str, save_path: str) -> dict:
    try:
        s = time.monotonic()
        response = ping(host, count=1, timeout=0.1)
        e = time.monotonic()
        #print(f"{e-s} sec.", host, name, log, response.is_alive)
        if save_path:
            with open(f'{save_path}/{host}-{name}.txt', 'a') as f:
                f.write(f'host address: {host} | host name: {name} | status: {"alive" if response.is_alive==True else "dead"} | time: {datetime.datetime.now()}\n')
            return {host: 'alive'} if response.is_alive==True else {host: 'dead'}
        else:
            return {host: 'alive'} if response.is_alive==True else {host: 'dead'}
    except:
        return {host: 'alive'} if response.is_alive==True else {host: 'dead'}

def host_pipeline(hosts: List[str], names: List[str], save_path: str) -> List[dict]:
    status_list = [check_host(host=hosts[idx], name=names[idx], save_path=save_path) for idx in range(len(hosts))]
    return status_list


def get_mac_address(host: str) -> str:
    try:
        result = subprocess.check_output(['arp', '-a', host])
        result = result.decode('utf-8')
        mac_pattern = re.compile(r'(\b[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b')
        match = mac_pattern.search(result)
        if match:
            mac = match.group(0).replace('-', ':')
            return mac
        else: 
            return "not found"
    except:
        return "network error"


# https://www.macvendorlookup.com/api
def get_mac_info(mac: str) -> str:
    try:
        url = f'https://api.macvendors.com/{mac}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text
            return data
        else:
            return "not found"
    except:
        return "network error"



if __name__ == "__main__":
    hosts = ['192.168.0.2', '192.168.0.1']
    names = ['google', 'router']
    save_path = 'res'
    log = True
    while True:
        s = time.monotonic()
        status_list = host_pipeline(hosts=hosts, names=names, save_path=save_path)
        e = time.monotonic()
        print(status_list, f"{e-s} sec.")
        time.sleep(1)

