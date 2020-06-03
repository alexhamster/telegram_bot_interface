from controller import *
from asyncio import Queue
from cmd_handlers import UnknownCommandHandler
from cmd_handlers import LoadImageCommandHandler
from cmd_handlers import ValidationCommandHandler
from orm_model import *


def main():
    try:
        end_point = UnknownCommandHandler()
        img_saver = LoadImageCommandHandler('/home/soliaris/temp/', Session, next_handler=end_point)
        validator = ValidationCommandHandler(Session, next_handler=img_saver)

        run_bot(validator)
    except Exception as e:
        logger.critical('Crash! ' + repr(e))
        return -1


if __name__ == '__main__':
    main()

