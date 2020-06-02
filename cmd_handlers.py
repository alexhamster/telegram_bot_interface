from commands import ICommand
from commands import LoadImageCommand
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


class LoadImageCommandHandler(UnknownCommandHandler):

    def __init__(self, storage_path, db_session, next_handler=None):
        super().__init__(next_handler)
        self.db_session = db_session
        self.storage_path = storage_path

    def _save_to_local(self, storage_path, file):
        logger.info('Saved to local')

    def _write_record_to_db(self, session):
        logger.info('Wrote to db')

    def handle(self, command):
        logger.info('type info: ' + command.content_info)
        image = command.get_content()
        if image is None:
            command.status = 'Cant load file from telegram server'
            command.execute()
            return
        self._save_to_local('./', image)
        self._write_record_to_db(None)
        command.status = 'File saved'
        command.execute()
