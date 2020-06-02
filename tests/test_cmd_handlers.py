import pytest
from collections import namedtuple
from telebot import AsyncTeleBot


class FakeBot(AsyncTeleBot):
    def reply_to(self, message, text, **kwargs):
        pass


@pytest.fixture
def get_bot():
    bot = FakeBot('somerandomtoken12345678')
    return bot


@pytest.fixture
def get_text_message():
    UserMessage = namedtuple('UserMessage', ['content_type', 'message_id', 'from_user', 'date', 'text'])
    UserInfo = namedtuple('UserInfo', ['id', 'first_name', 'username', 'last_name', 'language_code'])
    user_info = UserInfo(193586211, 'Alex', 'superuser', None, 'ru')
    msg = UserMessage('text', 1002, user_info, 1591014702, '/start do 123')
    return msg


def test_unknown_cmd_handler_init_wrong_param():
    from cmd_handlers import UnknownCommandHandler
    with pytest.raises(TypeError):
        UnknownCommandHandler(5, ['hello'])


def test_unknown_cmd_handler_init_correct_param():
    from cmd_handlers import UnknownCommandHandler
    try:
        UnknownCommandHandler('return message')
    except TypeError:
        pytest.fail('Unexpected TypeError...')


def test_unknown_cmd_handler_correct_type(get_bot, get_text_message):
    from cmd_handlers import UnknownCommandHandler
    from commands import BaseCommand
    h = UnknownCommandHandler()
    cmd = BaseCommand(get_bot, get_text_message)
    try:
        h.handle(cmd)
    except TypeError:
        pytest.fail('Unexpected TypeError...')


def test_unknown_cmd_handler_incorrect_type_handle():
    from cmd_handlers import UnknownCommandHandler
    h = UnknownCommandHandler()
    with pytest.raises(TypeError):
        h.handle('Hello')
