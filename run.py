from controller import *
from asyncio import Queue
from cmd_handlers import UnknownCommandHandler
from cmd_handlers import RedirectFilesCommandHandler
from cmd_handlers import ValidationCommandHandler
from orm_model import *
from time import sleep
import random
from proxy_collector import get_proxy

import asyncio
from proxybroker import Broker


def load_proxy_list(path='./proxy'):
    result = []
    with open(path, 'r') as file:
        for line in file:
            record = line.split(':')
            result.append(record)
    return result


def main(refresh_proxy_list=False):
    if refresh_proxy_list:
        get_proxy()
    proxy_list = load_proxy_list()
    # init handler chain
    end_point = UnknownCommandHandler()
    img_saver = RedirectFilesCommandHandler(Session, next_handler=end_point)
    validator = ValidationCommandHandler(Session, next_handler=img_saver)
    # starting proxy brod  force
    for proxy in proxy_list:
        logger.info('Using proxy %s:%s' % (proxy[0], proxy[1]))
        exit_code = run_bot(validator, use_proxy=True, proxy_host=proxy[0], proxy_port=proxy[1])
        if not (exit_code == -1):  # in case of unknown error(despite proxy error)
            logger.critical('Crash for unknown reason...')
            return


if __name__ == '__main__':
    while True:
        logger.info('Starting new iteration of main')
        try:
            main(refresh_proxy_list=True)
        except Exception as e:
            logger.critical(repr(e))
