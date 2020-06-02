import pytest
from moks import *


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
