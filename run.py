from controller import *
from asyncio import Queue
from cmd_handlers import UnknownCommandHandler
from cmd_handlers import RedirectFilesCommandHandler
from cmd_handlers import ValidationCommandHandler
from orm_model import *

import asyncio
from proxybroker import Broker

PROXY_LIST = []


async def show(proxies):
    global PROXY_LIST
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        PROXY_LIST.append(proxy)


def get_proxy():  # get proxy from proxybroker
    logger.info('Getting new proxy...')
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTPS'], limit=5),
        show(proxies))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


def main():
    global PROXY_LIST
    # init handler chain
    end_point = UnknownCommandHandler()
    img_saver = RedirectFilesCommandHandler(Session, next_handler=end_point)
    validator = ValidationCommandHandler(Session, next_handler=img_saver)
    # starting proxy brod  force
    while True:
        for proxy in PROXY_LIST:
            logger.info('Using proxy %s:%s' % (proxy.host, proxy.port))
            exit_code = run_bot(validator, use_proxy=True, proxy_host=proxy.host, proxy_port=proxy.port)
            if not (exit_code == -1):  # in case of unknown error(despite proxy error)
                logger.critical('Crash for unknown reason...')
                return
        get_proxy()  # if proxy list is empty get fresh proxy


if __name__ == '__main__':
    main()
