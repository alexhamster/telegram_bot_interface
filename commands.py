from collections import namedtuple
from loguru import logger

SenderInfo = namedtuple('SenderInfo', ['id', 'username', 'first_name', 'last_name',
                                       'language_code', 'date'])


class ICommand:

    def __init__(self):
        self.sender_info = None
        self.sender_message = None
        self.content = None
        self.content_info = None
        self.command_str = None
        self.input_source = None
        self.status = None

    def get_content(self):  # return content like a file, image, sound and etc
        raise NotImplementedError

    def execute(self, *args, **kwargs):  # send reply to user
        raise NotImplementedError


class BaseCommand(ICommand):

    def __init__(self, input_bot, api_message):
        super(BaseCommand, self).__init__()
        self.input_source = input_bot  # bot that receive message
        self.sender_message = api_message  # message got from telegram api
        self.sender_info = self._select_sender_info(api_message)  # info about user that send request to bot
        self.command_str = self._select_command_str(api_message)  # raw command text
        self.status = 'None command status'  # some command status
        self.content = api_message.text
        self.content_info = api_message.content_type

    @staticmethod
    def _select_sender_info(api_message) -> SenderInfo:
        # Select sender info from message that got from api
        # like a user_id, char_id, username, time and etc...
        info = SenderInfo(api_message.from_user.id,
                          api_message.from_user.username,
                          api_message.from_user.first_name,
                          api_message.from_user.last_name,
                          api_message.from_user.language_code,
                          api_message.date)

        # logger.debug('Select user info', info)
        return info

    @staticmethod
    def _select_command_str(api_message) -> list:
        # select command from api_message and put it to list
        if not isinstance(api_message.text, str):
            raise TypeError('Cant select command text')
        command_str = api_message.text.split(' ')
        logger.debug('message string: ' + str(command_str))
        return command_str

    def get_content(self):
        return self.command_str

    def execute(self, *args, **kwargs):  # send reply to user
        self.input_source.reply_to(self.sender_message, self.status)
