"""
This is the entry point of the bot. main() init the chain of the command handlers
"""
from loguru import logger
from bot_interface.controller import run_bot
from bot_logic.cmd_handlers import ValidationCommandHandler, ChangeUserDataCommandHandler
from bot_logic.cmd_handlers import RedirectFilesCommandHandler, UnknownCommandHandler
from sqlalchemy.orm import sessionmaker, scoped_session
from bot_orm.orm_model import engine


def load_proxy_list(path='./proxy'):
    result = []
    with open(path, 'r') as file:
        for line in file:
            record = line.split(':')
            result.append(record)
    return result


def init_handler_chain():
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    # last handler that drops unknown commands
    end_point = UnknownCommandHandler()
    # redirect files from commands to the endpoint channel. Used database to contain statistic
    redirect_to_channel = RedirectFilesCommandHandler(Session, next_handler=end_point)
    # checks sender's(user's) rights using database
    validator = ValidationCommandHandler(Session, next_handler=redirect_to_channel)
    # handle commands from the endpoint channel to ban or unban users of bot. Uses database to change user's info
    ban_unban = ChangeUserDataCommandHandler(Session, next_handler=validator)
    return ban_unban


def main(use_proxy=False, refresh_proxy_list=False):
    """
    There is init a configuration of bot
    :param use_proxy: If True bot will use proxy from './proxy' file to get access to TelegramAPI
    :param refresh_proxy_list: If True bot will automatically search free working proxy and rewrite './proxy' file
    :return: In case of unknown error will return None
    """
    first_handler = init_handler_chain()
    # starting proxy brod  force
    if use_proxy:
        from proxy_collector import get_proxy
        if refresh_proxy_list:
            get_proxy()  # rewrite './proxy' file with new proxy
        proxy_list = load_proxy_list()
        for proxy in proxy_list:
            logger.info('Using proxy %s:%s' % (proxy[0], proxy[1]))
            exit_code = run_bot(first_handler, use_proxy=use_proxy, proxy_host=proxy[0], proxy_port=proxy[1])
            if not (exit_code == -1):  # in case of unknown error(despite proxy error)
                logger.critical('Crash for unknown reason...')
                return
    else:
        run_bot(first_handler)


if __name__ == '__main__':
    # auto restart bot cause of crash
    while True:
        logger.info('Starting new iteration of main')
        try:
            main()
        except Exception as e:
            logger.critical(repr(e))
