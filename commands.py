from collections import namedtuple
from loguru import logger
from enum import Enum

SenderInfo = namedtuple('SenderInfo', ['id', 'username', 'first_name', 'last_name',
                                       'language_code', 'date'])


class Action(Enum):
    DO_NOTHING = 0
    REDIRECT_DOCUMENT = 1
    LOAD_DOCUMENT = 2
    BAN_USER = 3
    UNBAN_USER = 4


class ICommand:

    def __init__(self):
        self.sender_info = None
        self.sender_message = None
        self.content = None
        self.content_info = None
        self.action = None
        self.input_source = None

    def get_content(self):  # return content like a file, image, sound and etc
        raise NotImplementedError

    def abort(self, abort_message):  # return user abort message
        raise NotImplementedError

    def execute(self, *args, **kwargs):  # send reply to user
        raise NotImplementedError


class BaseCommand(ICommand):

    def __init__(self, input_bot, api_message, channel_id, action=Action.DO_NOTHING):
        super().__init__()
        self.input_source = input_bot  # bot that receive message
        self.sender_message = api_message  # message got from telegram api
        self.sender_info = self._select_sender_info(api_message)  # info about user that send request to bot
        self.action = action  # flag for handlers
        self.content = api_message.text
        self.content_info = api_message.content_type
        self.channel_id = channel_id  # admin channel telegram id

    def replace_none(self, data):
        if data is None:
            return '404'
        if isinstance(data, str):
            try:
                t_data = data.lower()
            except Exception as e:
                return data
            if t_data in 'none':
                return '404'
            if t_data in 'null':
                return '404'
        return data

    def _select_sender_info(self, api_message):
        # Select sender info from message that got from api
        # like a user_id, char_id, username, time and etc...
        try:
            info = SenderInfo(self.replace_none(api_message.from_user.id),
                              self.replace_none(api_message.from_user.username),
                              self.replace_none(api_message.from_user.first_name),
                              self.replace_none(api_message.from_user.last_name),
                              self.replace_none(api_message.from_user.language_code),
                            self.replace_none(api_message.date))
        except Exception as e:
            logger.warning('Cant select user info!')
            return None
        # logger.debug('Select user info', info)
        return info

    def get_content(self):
        return None

    def abort(self, abort_message='Server error, request cant be handled'):
        self.input_source.reply_to(self.sender_message, abort_message, disable_notification=True)

    def execute(self, *args, **kwargs):  # send reply to user
        self.input_source.reply_to(self.sender_message, self.status, disable_notification=True)


class LoadImageCommand(BaseCommand):
    """
        Command for loading image from telegram to local storage
    """

    def __init__(self, input_bot, api_message, channel_id):
        super().__init__(input_bot, api_message, channel_id)
        self.action = Action.LOAD_DOCUMENT

    @staticmethod
    def _load_file_from_server(bot, file_id):
        try:
            file = bot.get_file(file_id)
            local_file = bot.download_file(file.file_path)
        except Exception as e:
            logger.warning('Cant download a file! ' + repr(e))
            return None
        return local_file

    def get_content(self):  # download image from server
        file_id = self.sender_message.photo[-1].file_id
        self.content = self._load_file_from_server(self.input_source, file_id)
        return self.content


class RedirectImageToChannel(BaseCommand):
    """
    Command to redirect image from user to some channel
    """

    def __init__(self, input_bot, api_message, channel_id):
        super().__init__(input_bot, api_message, channel_id)
        self.action = Action.REDIRECT_DOCUMENT

    def execute(self, *args, **kwargs):
        file_id = self.sender_message.photo[-1].file_id
        message = 'from %s via @%s' % (self.sender_info.first_name, self.input_source.get_me().username)
        self.input_source.send_message(self.channel_id, self.sender_info.id, disable_notification=True)
        self.input_source.send_photo(self.channel_id, file_id, message, disable_notification=True)
        log_info = 'image from %s was redirected to %s' % (self.sender_info.username, self.channel_id)
        logger.info(log_info)
        self.input_source.reply_to(self.sender_message, 'Done!')


class RedirectDocumentToChannel(BaseCommand):
    """
    Command to redirect documents from user to some channel
    """

    def __init__(self, input_bot, api_message, channel_id):
        super().__init__(input_bot, api_message, channel_id)
        self.action = Action.REDIRECT_DOCUMENT

    def execute(self, *args, **kwargs):
        file_id = self.sender_message.document.file_id
        message = 'from %s via @%s' % (self.sender_info.first_name, self.input_source.get_me().username)
        self.input_source.send_message(self.channel_id, self.sender_info.id, disable_notification=True)
        self.input_source.send_document(self.channel_id, file_id, caption=message, disable_notification=True)
        log_info = 'document from %s was redirected to %s' % (self.sender_info.username, self.channel_id)
        logger.info(log_info)
        self.input_source.reply_to(self.sender_message, 'Done!')


class RedirectLinkToChannel(BaseCommand):
    """
    Command to redirect link from user to some channel
    """

    def __init__(self, input_bot, api_message, channel_id):
        super().__init__(input_bot, api_message, channel_id)
        self.action = Action.REDIRECT_DOCUMENT

    def execute(self, *args, **kwargs):
        self.input_source.send_message(self.channel_id, self.sender_info.id)
        self.input_source.send_message(self.channel_id, self.sender_message.text)
        log_info = 'Link from %s was redirected to %s' % (self.sender_info.username, self.channel_id)
        logger.info(log_info)
        self.input_source.reply_to(self.sender_message, 'Done!')


class BanOrUnbanUserCommand(BaseCommand):
    """
    That command select from text user id that will be banned
    """
    def __init__(self, input_bot, api_message, channel_id, ban=True):
        super().__init__(input_bot, api_message, channel_id)
        if ban:
            self.action = Action.BAN_USER
        else:
            self.action = Action.UNBAN_USER
        self.sender_info = SenderInfo(self.select_user_id_from_message(api_message.reply_to_message.text),
                                      None, None, None, None, None)

    def select_user_id_from_message(self, api_message_text) -> int:
        # selects user id from message text
        user_id = None
        try:
            user_id = int(api_message_text)
        except Exception as e:
            logger.warning('Cant select id from text' + repr(e))
        return user_id

    def execute(self, *args, **kwargs):
        if self.action == Action.BAN_USER:
            self.input_source.reply_to(self.sender_message, 'User with id: %s was banned!' % self.sender_info.id,
                                       disable_notification=True)
        else:
            self.input_source.reply_to(self.sender_message, 'User with id: %s was unbanned!' % self.sender_info.id,
                                       disable_notification=True)
