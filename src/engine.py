import asyncio
import aiofile
from icmplib import ping
import datetime
from typing import List

async def check_host(host: str, name: str, save_path: str, log: bool = True) -> None:
    response = ping(host, count=1, timeout=0.1)
    async with aiofile.AIOFile(f'{save_path}/{host}.txt', 'a') as afp:
        if log:
            await afp.write(f'host address: {host} | host name {name} | status: {"alive" if response.is_alive==True else "dead"} | time: {datetime.datetime.now()}\n')
        else:
            if response.is_alive == False:
                await afp.write(f'host address: {host} | host name {name} | status: {"alive" if response.is_alive==True else "dead"} | time: {datetime.datetime.now()}\n')
                
async def host_pipeline(hosts: List[str], names: str, save_path: str, ) -> None:
    await asyncio.gather(*[check_host(host=hosts[idx], name=names[idx], save_path=save_path) for idx in range(len(hosts))])

