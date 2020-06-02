from controller import *
from asyncio import Queue
from cmd_handlers import UnknownCommandHandler
from cmd_handlers import LoadImageCommand

if __name__ == '__main__':
    handler = LoadImageCommandHandler('/home/soliaris/temp/', None)
    run_bot(handler)