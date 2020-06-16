import asyncio
import random

import aiohttp
from proxybroker.resolver import Resolver
from proxybroker.utils import log

import asyncio
from proxybroker import Broker
"""
Generate a file(./proxy) with a lot of proxy
"""


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


def write_to_file(proxy_list, path='./proxy'):
    with open(path, 'a') as file:
        for i in proxy_list:
            proxy_string = str(i.host) + ':' + str(i.port) + '\n'
            file.write(proxy_string)


if __name__ == "__main__":
    proxies = asyncio.Queue()  # coroutine queue
    broker = Broker(proxies, timeout=8)
    promise = asyncio.gather(broker.find(types=['HTTPS'], limit=100), get_stuff(proxies))
    loop = asyncio.get_event_loop()
    _, proxy_list = loop.run_until_complete(promise) # returns as many values, as many tasks we have
    write_to_file(proxy_list)

# TODO Сделать проверку на None имен пользователя