from commands import ICommand
from commands import LoadImageCommand
from loguru import logger  # for logging
from abc import *
from orm_model import User


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

    def __init__(self, reply='Unknown command'):
        super().__init__()
        if not isinstance(reply, str):
            raise TypeError('reply must to be a string!')
        self._reply_to_user = reply
        self._next_handler = None

    def handle(self, command):
        if not isinstance(command, ICommand):
            raise TypeError('UnknownCommandHandler can work only with ICommand interface from commands.py!')
        if command is None:
            raise TypeError('Command cant be None')

        logger.info('Unknown command: ' + str(command.command_str))
        command.status = self._reply_to_user
        command.execute()


class LoadImageCommandHandler(UnknownCommandHandler):

    def __init__(self, storage_path, SessionFactory, next_handler=None):
        super().__init__()
        self.SessionFactory = SessionFactory
        self.storage_path = storage_path
        self._next_handler = next_handler

    def _save_to_local(self, storage_path, file_name, file):
        try:
            with open(storage_path + file_name, 'wb') as new_file:
                new_file.write(file)
                new_file.close()
        except Exception:
            logger.warning('Cant save file to local storage')
            return
        logger.info('File saved to local storage')

    def _write_record_to_db(self, session, command):
        logger.info('Wrote to db')

    @property
    def next_handler(self):
        return self._next_handler

    @next_handler.setter
    def next_handler(self, value):
        if value is self._next_handler:
            raise RuntimeError('Next handler cant be the same handler')
        self._next_handler = value

    def change_users_record(self, command):  # TODO put it in more appropriate handler
        """
        Change in db users post_count and recent_count. Add them +1
        """
        try:
            sess = self.SessionFactory()
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

        if not command.sender_message.content_type == 'photo':
            if not (self._next_handler is None):
                self._next_handler.handle(command)

        self.change_users_record(command)  # TODO put it in more appropriate handler

        logger.info('type info: ' + command.content_info)
        image = command.get_content()
        if image is None:
            logger.warning('Command content is None, cant handle photo!')
            command.status = 'Cant load file from telegram server'
            command.execute()
            return
        self._save_to_local(self.storage_path, str(command.sender_message.date), image)
        self._write_record_to_db(None, None)
        command.status = 'File saved'
        command.execute()


class ValidationCommandHandler(UnknownCommandHandler):
    """
    That handler drops command from banned users and spam commands.
    It checks in the DB user status and count of resent images.
    """

    def __init__(self, SessionFactory, next_handler):
        super().__init__()
        self.next_handler = next_handler
        self.SessionFactory = SessionFactory

    def add_new_user(self, command):
        user_info = {
            'id': command.sender_info.id,
            'name': command.sender_info.first_name,
            'username': command.sender_info.username,
        }
        try:
            sess = self.SessionFactory()
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
        sess = self.SessionFactory()
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
            logger.info('Status of %s if OK' % command.sender_info.username)
            return False
        logger.warning('Request from %s was rejected cause of ban.' % command.sender_info.username)
        return True

    def is_above_limit(self, command, limit=20) -> bool:
        """
        Checking user resent post count and return True if count is above the limit
        """
        sess = self.SessionFactory()
        recent_count = sess.query(User.recent_count).filter(User.id == command.sender_info.id).first()
        if recent_count[0] > limit:
            logger.warning('Above the limit, post from %s dropped' % command.sender_info.username)
            return True
        return False

    def handle(self, command):
        if self.user_is_banned(command):
            command.abort('You are was banned by an administrator of the bot')
            return

        if self.is_above_limit(command):
            command.abort('You reach your daily post limit for today, try tomorrow :)')
            return

        if self.next_handler is None:
            logger.warning('After ValidationCommandHandler next is none')
            return
        self.next_handler.handle(command)
