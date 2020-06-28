"""
There ara command handler that contain main logic of the bot. Command handlers works with ICommand interface from
commands.py.
Handlers organized like a chain(unidirectional linked list). Command get from head to tail.
https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern
https://en.wikipedia.org/wiki/Command_pattern
"""
from abc import ABCMeta, abstractmethod
import time
from loguru import logger
from .commands import ICommand
from bot_orm.orm_model import User
from .commands import ActionEnum  # used in handlers for catching commands
from config import *


class ICommandHandler(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        self._next_handler = None

    @abstractmethod
    def handle(self, command):
        pass


class UnknownCommandHandler(ICommandHandler):
    """
    Handle all unknown commands. Works with ICommand interface.
    """

    def __init__(self, db_session_class=None, next_handler=None):
        super().__init__()
        self._next_handler = next_handler
        self.db_session_class = db_session_class

    @property
    def next_handler(self):
        return self._next_handler

    @next_handler.setter
    def next_handler(self, value):
        if value is self._next_handler:
            raise RuntimeError('Next handler cant be the same handler')
        self._next_handler = value

    def handle(self, command):
        if not isinstance(command, ICommand):
            raise TypeError('UnknownCommandHandler can work only with ICommand interface from commands.py!')
        if command is None:
            raise TypeError('Command cant be None')

        logger.info('Unknown command: ' + str(command.command_str))
        command.abort(UNKNOWN_COMMAND_MESSAGE)


class ChangeUserDataCommandHandler(UnknownCommandHandler):
    """
    Handle commands that changes user data in database
    """

    def __init__(self, db_session_class, next_handler=None):
        super().__init__(db_session_class, next_handler)

    def handle(self, command):
        if not isinstance(command, ICommand):
            raise TypeError('LoadImageCommandHandler can work only with ICommand interface from commands.py!')
        if command is None:
            raise TypeError('Command cant be None')

        if not (command.action == ActionEnum.BAN_USER or command.action == ActionEnum.UNBAN_USER):
            if not (self.next_handler is None):
                self.next_handler.handle(command)
                return
            command.abort('Cant handle that request')

        if command.sender_info.id is None:
            command.abort('Selection of user id was unsuccessful')
            return
        try:
            sess = self.db_session_class()
            if command.action == ActionEnum.BAN_USER:
                sess.query(User.status).filter(User.id == command.sender_info.id).update({'status': 0})
            if command.action == ActionEnum.UNBAN_USER:
                sess.query(User.status).filter(User.id == command.sender_info.id).update({'status': 1})
            sess.commit()
            command.execute()
            logger.warning('Users status was changed')
        except Exception as e:
            logger.warning('Cant change users status' + repr(e))
            command.abort('Cant change status of that user')


class RedirectFilesCommandHandler(UnknownCommandHandler):
    """
    Handle a redirection command. Change record about user, when command is handled.
    Needs sqlalchemy session factory for working with DB.
    """

    def __init__(self, db_session_class, next_handler=None):
        super().__init__(db_session_class, next_handler)

    def change_users_record(self, command):
        """
        Change in db users post_count and recent_count. Add them +1
        """
        try:
            sess = self.db_session_class()
            sess.query(User.post_count, User.recent_count). \
                filter(User.id == command.sender_info.id). \
                update({"post_count": (User.post_count + 1),
                        "recent_count": (User.recent_count + 1)})
            sess.commit()
        except Exception as e:
            logger.error('Cant update user status in db. Username: %s, Reason: %s' % (command.sender_info.username,
                                                                                      repr(e)))

    def handle(self, command):
        if not isinstance(command, ICommand):
            raise TypeError('LoadImageCommandHandler can work only with ICommand interface from commands.py!')
        if command is None:
            raise TypeError('Command cant be None')

        if not command.action == ActionEnum.REDIRECT_DOCUMENT:
            if not (self.next_handler is None):
                self.next_handler.handle(command)
                return
            command.abort('Cant handle that request')

        self.change_users_record(command)
        command.execute()


class ValidationCommandHandler(UnknownCommandHandler):
    """
    That handler drops command from banned users and spam commands.
    It checks in the DB user status and count of resent images.
    """

    def __init__(self, db_session_class, next_handler):
        super().__init__(db_session_class, next_handler)
        self.post_limit_for_user = MAXIMUM_POSTS_PER_TIME_INTERVAL  # limit for every user for posting
        self.limit_time_interval_s = TIME_INTERVAL_S  # amount of time, when people can send

    def add_new_user(self, command):
        user_info = {
            'id': command.sender_info.id,
            'name': command.sender_info.first_name,
            'username': command.sender_info.username,
            'when_started': time.time()
        }
        try:
            sess = self.db_session_class()
            sess.add(User(**user_info))
            sess.commit()
        except Exception as e:
            logger.warning('Cant add new user! ' + repr(e))
        logger.info('New user added! name: ' + user_info['username'])

    def user_is_banned(self, command) -> bool:
        """
        get user status from the db and return True if status is 0(banned)
        If there is no user in database it will create it
        """
        status = 0
        sess = self.db_session_class()
        try:
            status = sess.query(User.status).filter(User.id == command.sender_info.id).first()
            if status is None:
                self.add_new_user(command)  # add new user to db if we cant find record about him
                logger.info('User %s was added to database' % command.sender_info.username)
                return False
        except Exception as e:
            logger.warning('Cant read user status from db! ' + repr(e))
            return True
        if status[0] == 1:
            logger.info('Status of %s is OK' % command.sender_info.username)
            return False
        logger.warning('Request from %s was rejected cause of ban.' % command.sender_info.username)
        return True

    def is_above_limit(self, command, post_limit=10, time_interval_s=3600) -> bool:
        """
        Checking user resent post count and return True if count is above the limit
        """
        sess = self.db_session_class()
        user = sess.query(User).filter(User.id == command.sender_info.id).first()
        if user.recent_count >= post_limit:
            if (time.time() - user.when_started) < time_interval_s:
                logger.warning('Above the limit, post from %s dropped' % command.sender_info.username)
                return True
        if (time.time() - user.when_started) > time_interval_s:
            user.recent_count = 0
            user.when_started = time.time()
        sess.commit()
        return False

    def handle(self, command):
        if self.user_is_banned(command):
            command.abort(BAN_MESSAGE)
            return

        if self.is_above_limit(command, post_limit=self.post_limit_for_user,
                               time_interval_s=self.limit_time_interval_s):
            command.abort(POST_LIMIT_MESSAGE %
                          (self.post_limit_for_user,
                           round(self.limit_time_interval_s / 60)))
            return

        if self.next_handler is None:
            logger.warning('After ValidationCommandHandler next is None. Maybe an error?')
            return
        self.next_handler.handle(command)
