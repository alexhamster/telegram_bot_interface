from sqlalchemy import create_engine, ForeignKey
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship, session, sessionmaker, scoped_session

Base = declarative_base()
engine = create_engine('sqlite:///tg_bot.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)  # user id from telegram api
    name = Column('name', String, nullable=False)  # first name in telegram
    username = Column('username', String, nullable=False)  # username in telegram
    post_count = Column('post_count', Integer, default=0, nullable=False)  # how many posts user send
    status = Column('status', Integer, nullable=False, default=1)  # status. 0 - banned, 1 - default
    recent_count = Column('recent_count', Integer, default=0, nullable=False)  # recent posts count
    when_started = Column('when_started', Float, default=0, nullable=False)  # time till first post from user


def db_init():
    print('Clear db inited!')
    Base.metadata.create_all(engine)  # create tables, use ONE TIME


if __name__ == "__main__":
    db_init()
