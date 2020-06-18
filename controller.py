"""
In that file we handle requests from Telegram API. For different requests
it makes concrete command objects from commands.py
"""

import telebot  # for bot api
from telebot import apihelper  # for proxy support
from config import *  # config file
from loguru import logger  # for logging
from commands import BaseCommand
from commands import RedirectDocumentToChannel
from commands import RedirectImageToChannel
from commands import RedirectLinkToChannel
from cmd_handlers import *
from requests.exceptions import ProxyError

BOT = telebot.TeleBot(TOKEN, threaded=False)
logger.add("./logs/file_{time}.log")
HANDLERS_HEAD = None  # ref to first handler in the handlers chain


def get_short_info(message):
    return ' From ' + str(message.from_user) + ' Message text: ' + str(message.text)


@BOT.message_handler(commands=['start'])
def start(message):
    logger.info('Incoming start message: %s' % get_short_info(message))
    BOT.reply_to(message, START_MESSAGE)


@BOT.message_handler(commands=['help'])
def start(message):
    logger.info('Incoming help message: %s' % get_short_info(message))
    BOT.reply_to(message, HELP_MESSAGE)


@BOT.channel_post_handler(commands=['init'])
def channel(message):
    print(message)
    OUT_CHANEL_ID = message.chat.id
    BOT.reply_to(message, 'Admin channel inited! ID:%s' % OUT_CHANEL_ID)


@BOT.message_handler(content_types=['photo'])
def photo(message):  # handle photo from user
    logger.info('Incoming photo %s' % get_short_info(message))
    redirect = RedirectImageToChannel(BOT, message, OUT_CHANEL_ID)
    HANDLERS_HEAD.handle(redirect)


@BOT.message_handler(content_types=['document'])
def photo(message):  # handle document from user
    logger.info('Incoming document %s' % get_short_info(message))
    redirect = RedirectDocumentToChannel(BOT, message, OUT_CHANEL_ID)
    HANDLERS_HEAD.handle(redirect)


@BOT.message_handler(regexp="http[s]*:\/\/[0-9a-z./A-Z@#!_-]*")
def handle_message(message):
    logger.info('Incoming link %s' % get_short_info(message))
    redirect = RedirectLinkToChannel(BOT, message, OUT_CHANEL_ID)
    HANDLERS_HEAD.handle(redirect)


@BOT.message_handler(func=lambda m: True)
def echo_all(message):
    logger.info('Unknown message %s' % get_short_info(message))
    BOT.reply_to(message, 'Cant handle this')


def run_bot(start_handler, use_proxy=False, proxy_host='', proxy_port=''):
    if not isinstance(start_handler, ICommandHandler):
        raise TypeError('run_bot() needs ICommandHandler object as a first param')

    logger.info('Bot started.')
    if use_proxy:
        try:
            apihelper.proxy = {'https': 'https://%s:%s' % (proxy_host,
                                                           proxy_port)}
        except ProxyError as e:
            logger.warning('Invalid proxy %s:%s' % (proxy_host, proxy_port))
            return -1
    try:
        global HANDLERS_HEAD
        HANDLERS_HEAD = start_handler
        BOT.polling(timeout=5)  # start bot handler loop
    except Exception as pe:
        logger.warning('Proxy %s:%s is dead... %s' % (proxy_host, proxy_port, repr(pe)))
        return -1
    return -2
