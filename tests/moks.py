import pytest
from collections import namedtuple
from telebot import AsyncTeleBot

class FakeBot(AsyncTeleBot):
    def reply_to(self, message, text, **kwargs):
        pass

    def get_file_url(self, file_id):
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
