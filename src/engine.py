from icmplib import ping
import datetime
from typing import List
import time

def check_host(host: str, name: str, save_path: str) -> dict:
    try:
        s = time.monotonic()
        response = ping(host, count=1, timeout=0.1)
        e = time.monotonic()
        #print(f"{e-s} sec.", host, name, log, response.is_alive)
        if save_path:
            with open(f'{save_path}/{host}-{name}.txt', 'a') as f:
                f.write(f'host address: {host} | host name: {name} | status: {"alive" if response.is_alive==True else "dead"} | avg_time: {response.avg_rtt} | time: {datetime.datetime.now()}\n')
                complete_status = {host: 'alive', 'name': name, 'avg_time': response.avg_rtt} if response.is_alive==True else {host: 'dead', 'name': name, 'avg_time': response.avg_rtt}
                simple_status = {host: 'alive'} if response.is_alive==True else {host: 'dead'}
            return [simple_status, complete_status]
        else:
            complete_status = {host: 'alive', 'name': name, 'avg_time': response.avg_rtt} if response.is_alive==True else {host: 'dead', 'name': name, 'avg_time': response.avg_rtt}
            simple_status = {host: 'alive'} if response.is_alive==True else {host: 'dead'}
            return [simple_status, complete_status]
    except:
        complete_status = {host: 'alive', 'name': name, 'avg_time': response.avg_rtt} if response.is_alive==True else {host: 'dead', 'name': name, 'avg_time': response.avg_rtt}
        simple_status = {host: 'alive'} if response.is_alive==True else {host: 'dead'}
        return [simple_status, complete_status]


def host_pipeline(hosts: List[str], names: List[str], save_path: str) -> List[dict]:
    status_list = [check_host(host=hosts[idx], name=names[idx], save_path=save_path) for idx in range(len(hosts))]
    return status_list

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

