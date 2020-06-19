# ===GENERAL===
DEBUG = False
TOKEN = ''
OUT_CHANEL_ID = ''
if DEBUG is True:
    TOKEN = '237864712:AAFCGxye9gCoj5hWi7QStPV8TEpXO933PJo'
    OUT_CHANEL_ID = -1001224201477  # TODO менять автоматически!
else:
    TOKEN = '1266408358:AAEhtq_AquzDszkN1XQOB6G0ERpVPrPbkXM'
    OUT_CHANEL_ID = -1001150073760  # TODO менять автоматически!

# ===MESSAGE_PACK===
# This is message pack, that bot will send to users
START_MESSAGE = 'Hello, i am bot for t.me/waifu_paradise chanel suggestions. Send me something(images, gifs, ' \
                'links) you want to see in ' \
                'the chanel. '
HELP_MESSAGE = 'Just send me anime ;) Image, gif or maybe link. In case of errors write to https://t.me/waifuchat'

POST_LIMIT_MESSAGE = 'Above the post limit! You can send %s posts every %s minute(s)'

BAN_MESSAGE = 'Error number 69, please write about it in https://t.me/waifuchat'

UNKNOWN_COMMAND_MESSAGE = 'Cant handle that request'

SUCCESS_MESSAGE = 'Done!'

# ===INNER_CONFIGURATION===

MAXIMUM_POSTS_PER_TIME_INTERVAL = 10  # How many posts from user will handle bot during one time interval

TIME_INTERVAL_S = 60*30  # Duration of one time interval in seconds

