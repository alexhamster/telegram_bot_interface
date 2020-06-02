from controller import *
from asyncio import Queue
from cmd_handlers import UnknownCommandHandler

if __name__ == '__main__':
    handler = UnknownCommandHandler(None, 'Hello world!')
    run_bot(handler)