"""
This is the main configuration file of the bot. Here you can define a bot token, an endpoint channel id,
a database, a message pack and anti-spam configuration.
"""

# ===GENERAL===
# WARNING! keep your bot Token in secret! In case of leakage generate new one.
TOKEN = ''  # Use telegram father bot to get that token
# To find out OUT_CHANEL_ID add a bot to your channel and write '/init'. Then copy an id and paste it below
OUT_CHANEL_ID = -1


DATABASE = 'sqlite:///tg_bot.db'  # WARNING, there is no guarantee about working with other databases

# ===MESSAGE_PACK===
# This is message pack, that bot will send to users depends on their actions

START_MESSAGE = 'Hello, i am bot for chanel suggestions. Send me something(images, gifs, ' \
                'links) you want to see in ' \
                'the chanel. '
HELP_MESSAGE = 'Just send me something ;) Image, gif or maybe link.'

POST_LIMIT_MESSAGE = 'Above the post limit! You can send %s posts every %s minute(s)'

BAN_MESSAGE = 'You was banned by administrator'

UNKNOWN_COMMAND_MESSAGE = 'Cant handle that request'

SUCCESS_MESSAGE = 'Done!'

# ===ANTI_SPAM_CONFIGURATION===
# That vars define how many and how often users can send content(photo, gifs, links) to endpoint channel

MAXIMUM_POSTS_PER_TIME_INTERVAL = 10  # How many content posts from user will handle bot during one time interval

TIME_INTERVAL_S = 60*30  # Duration of one time interval in seconds

