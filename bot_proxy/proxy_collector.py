"""
There are functions to make proxy file using proxybroker(https://github.com/constverum/ProxyBroker).
Bot can use file 'proxy' to get access to TelegramAPI in case of government blocking
"""
import asyncio
import aiohttp
import random
import requests
from pathlib import Path
from proxybroker import Broker
from proxybroker.resolver import Resolver
from proxybroker.utils import log


async def get_stuff(proxies: asyncio.Queue):
    result = []
    counter = 1
    while proxies:
        proxy = await proxies.get()
        if proxy is None: break
        result.append(proxy)
        print('Added proxy %s' % counter)
        counter += 1
    return result


def ping_proxy(host, port) -> bool:
    # Check proxy with ping https://telegram.org
    if not (isinstance(host, str) and isinstance(port, str)):
        return False
    try:
        s = requests.Session()
        s.proxies = {'https': 'https://%s:%s' % (host, port)}
        r = s.get('https://telegram.org', timeout=1)
        s.close()
    except Exception as e:
        print(repr(e))
        return False
    else:
        return True


def write_to_file(proxy_list, path='./proxy'):
    try:
        if not Path(path).is_file():
            f = open(path, "w")
            f.close()
        with open(path, 'w') as file:
            for i in proxy_list:
                if not ping_proxy(str(i.host), str(i.port)):
                    continue
                proxy_string = str(i.host) + ':' + str(i.port) + '\n'
                file.write(proxy_string)
    except Exception as e:
        print(repr(e))
        return False
    return True


def get_proxy():
    proxies = asyncio.Queue()  # coroutine queue
    broker = Broker(proxies, timeout=8)
    promise = asyncio.gather(broker.find(types=['HTTPS'], limit=100), get_stuff(proxies))
    loop = asyncio.get_event_loop()
    _, proxy_list = loop.run_until_complete(promise)  # returns as many values, as many tasks we have
    write_to_file(proxy_list)


# To get new proxy file just run using console
if __name__ == "__main__":
    get_proxy()
