import telebot  # for bot api
from telebot import apihelper  # for proxy support
from config import *  # config file
from loguru import logger  # for logging
from commands import BaseCommand
from commands import LoadImageCommand
from commands import RedirectImageToChannel
from cmd_handlers import *
# # for transport commands to other proc

BOT = telebot.TeleBot(TOKEN)
logger.add("./logs/file_{time}.log")
HANDLERS_HEAD = None


@BOT.message_handler(commands=['start'])
def start(message):
    logger.info('Incoming message: ' + message.text)
    start_command = BaseCommand(BOT, message)
    HANDLERS_HEAD.handle(start_command)


@BOT.message_handler(commands=['t'])
def start(message):
    print(message)


@BOT.channel_post_handler(commands=['/stat'])
def channel(message):
    BOT.reply_to(message, 'All OK')


@BOT.message_handler(content_types=['photo'])
def photo(message):  # handle photo from user
    logger.info('Incoming photo from: ')
    chanel_id = -1001150073760
    redirect = RedirectImageToChannel(BOT, message, chanel_id)
    HANDLERS_HEAD.handle(redirect)


def run_bot(start_handler):
    if not isinstance(start_handler, ICommandHandler):
        raise TypeError('run_bot() needs ICommandHandler object as a first param')

    logger.info('Bot started.')
    if USE_PROXY:
        apihelper.proxy = {'https': 'https://%s:%s@%s:%s' % (PROXY_LOGIN,
                                                             PROXY_PASS,
                                                             PROXY_IP,
                                                             PROXY_HTTP_PORT)}
    global HANDLERS_HEAD
    HANDLERS_HEAD = start_handler
    BOT.polling()  # start bot handler loop




