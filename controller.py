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

# # for transport commands to other proc

BOT = telebot.TeleBot(TOKEN)
logger.add("./logs/file_{time}.log")
HANDLERS_HEAD = None


@BOT.message_handler(commands=['start'])
def start(message):
    logger.info('Incoming message: ' + message.text)
    start_message = 'Hello, i am bot for t.me/waifu_paradise chanel suggestions. Send me something(images, gifs, ' \
                    'links) you want to see in ' \
                    'the chanel. '
    BOT.reply_to(message, start_message)


@BOT.message_handler(commands=['help'])
def start(message):
    logger.info('Incoming message: ' + message.text)
    help_msg = 'Just send me anime ;) Image, gif or maybe link.'
    BOT.reply_to(message, help_msg)


@BOT.channel_post_handler(commands=['stat'])
def channel(message):
    BOT.reply_to(message, 'All OK')


@BOT.message_handler(content_types=['photo'])
def photo(message):  # handle photo from user
    logger.info('Incoming photo from: ' + message.from_user.username)
    chanel_id = -1001150073760
    redirect = RedirectImageToChannel(BOT, message, chanel_id)
    HANDLERS_HEAD.handle(redirect)


@BOT.message_handler(content_types=['document'])
def photo(message):  # handle photo from user
    logger.info('Incoming document from: ' + message.from_user.username)
    chanel_id = -1001150073760
    redirect = RedirectDocumentToChannel(BOT, message, chanel_id)
    HANDLERS_HEAD.handle(redirect)


@BOT.message_handler(regexp="http[s]*:\/\/[0-9a-z./A-Z@#!_-]*")
def handle_message(message):
    logger.info('Incoming link from: ' + message.from_user.username)
    chanel_id = -1001150073760
    redirect = RedirectLinkToChannel(BOT, message, chanel_id)
    HANDLERS_HEAD.handle(redirect)


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
        BOT.polling()  # start bot handler loop
    except Exception as pe:
        logger.warning('Proxy %s:%s is dead... %s' % (proxy_host, proxy_port, repr(pe)))
        return -1
    return -2
