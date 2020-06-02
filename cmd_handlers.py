from commands import ICommand
from loguru import logger  # for logging
from abc import *


class ICommandHandler(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        self.next_handler = None

    @abstractmethod
    def handle(self, command):
        pass


class UnknownCommandHandler(ICommandHandler):
    """
    Handle all unknown commands. Works with ICommand interface.
    """

    def __init__(self, next_handler=None, reply='Unknown command'):
        super().__init__()
        if not isinstance(reply, str):
            raise TypeError('reply must to be a string!')
        self._reply_to_user = reply
        self.next_handler = next_handler

    @property
    def next_handler(self):
        return self.next_handler

    @next_handler.setter
    def next_handler(self, value):
        self._next_handler = value

    def handle(self, command):
        if not isinstance(command, ICommand):
            raise TypeError('UnknownCommandHandler can work only with ICommand interface from commands.py!')
        logger.info('Unknown command: ' + str(command.command_str))
        command.status = self._reply_to_user
        command.execute()


