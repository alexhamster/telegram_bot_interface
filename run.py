from controller import *
from asyncio import Queue
from cmd_handlers import UnknownCommandHandler
from cmd_handlers import RedirectFilesCommandHandler
from cmd_handlers import ValidationCommandHandler
from orm_model import *
from time import sleep
import random

import requests

import asyncio
from proxybroker import Broker


def load_proxy_list(path='./proxy'):
    result = []
    with open(path, 'r') as file:
        for line in file:
            record = line.split(':')
            result.append(record)
    return result


def ping_proxy(host, port) -> bool:
    if not (isinstance(host, str) and isinstance(port, str)):
        return False
    try:
        s = requests.Session()
        s.proxies = {'https': 'https://%s:%s' % (host, port)}
        r = s.get('https://ya.ru', timeout=2)
        s.close()
    except Exception as e:
        print(repr(e))
        return False
    else:
        return True

def main():
    proxy_list = load_proxy_list()
    random.seed()
    random.shuffle(proxy_list)
    # init handler chain
    end_point = UnknownCommandHandler()
    img_saver = RedirectFilesCommandHandler(Session, next_handler=end_point)
    validator = ValidationCommandHandler(Session, next_handler=img_saver)
    # starting proxy brod  force
    for proxy in proxy_list:
        if not ping_proxy(proxy[0], proxy[1]):
            logger.warning('Invalid proxy %s:%s' % (proxy[0], proxy[1]))
            continue
        logger.info('Using proxy %s:%s' % (proxy[0], proxy[1]))
        exit_code = run_bot(validator, use_proxy=True, proxy_host=proxy[0], proxy_port=proxy[1])
        if not (exit_code == -1):  # in case of unknown error(despite proxy error)
            logger.critical('Crash for unknown reason...')
            return
        #proxy_list = load_proxy_list()  # if proxy list is empty get fresh proxy


if __name__ == '__main__':
    while True:
        logger.info('Starting new iteration of main')
        try:
            main()
        except Exception as e:
            logger.warning(repr(e))
