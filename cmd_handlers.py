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
        if command is None:
            raise TypeError('Command cant be None')

        logger.info('Unknown command: ' + str(command.command_str))
        command.status = self._reply_to_user
        command.execute()


class LoadImageCommandHandler(UnknownCommandHandler):

    def __init__(self, storage_path, db_session, next_handler=None):
        super().__init__(next_handler)
        self.db_session = db_session
        self.storage_path = storage_path

    def _save_to_local(self, storage_path, file_name, file):
        try:
            with open(storage_path + file_name, 'wb') as new_file:
                new_file.write(file)
                new_file.close()
        except Exception:
            logger.warning('Cant save file to local storage')
            return
        logger.info('File saved to local storage')


    def _write_record_to_db(self, session):
        logger.info('Wrote to db')

    def handle(self, command):
        if not isinstance(command, ICommand):
            raise TypeError('LoadImageCommandHandler can work only with ICommand interface from commands.py!')
        if command is None:
            raise TypeError('Command cant be None')

        if not command.sender_message.content_type == 'photo':
            self.next_handler.handle(command)

        logger.info('type info: ' + command.content_info)
        image = command.get_content()
        if image is None:
            command.status = 'Cant load file from telegram server'
            command.execute()
            return
        self._save_to_local(self.storage_path, str(command.sender_message.date), image)
        self._write_record_to_db(None)
        command.status = 'File saved'
        command.execute()
