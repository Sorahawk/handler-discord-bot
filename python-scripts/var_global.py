import sys


### LINUX ###

# absolute path to the project folder on the Linux cloud instance
# cannot use os.getcwd() because systemd service runs the script from root directory
LINUX_ABSOLUTE_PATH = '/home/ubuntu/handler-bot/python-scripts'

# name of the bot service running on the Linux cloud instance
LINUX_SERVICE_NAME = 'handler-bot.service'


### DISCORD ###

# ID of Discord server channel to send news notifications
NEWS_CHANNEL_ID = 1356173681369415871

# ID of Discord server channel to send Wilds info notifications
INFO_CHANNEL_ID = 1365653663238066207

# ID of Discord server channel to send event quest notifications
QUEST_CHANNEL_ID = 1349006234375950337

# news channel object, to be initialised when the bot calls on_ready()
NEWS_CHANNEL = None

# info channel object, to be initialised when the bot calls on_ready()
INFO_CHANNEL = None

# quest channel object, to be initialised when the bot calls on_ready()
QUEST_CHANNEL = None

# Discord server role name to ping for notifications
NOTIFY_ROLE_NAME = '<@&1097703521886941274>'


### MAIN ###

BOT_INSTANCE = None

# symbol to signify bot commands
BOT_COMMAND_PREFIX = '.'

# list of bot commands
BOT_COMMAND_LIST = ['quest', 'update']

# dictionary of command flags
# each flag can only be a single letter
BOT_COMMAND_FLAGS = { 'all': 'a' }

# proxy URL to route web traffic through
PROXY_URL = 'http://gw.dataimpulse.com:823'

# standard headers for HTTP requests
STANDARD_HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }

# URL for Japanese News webpage
JAPANESE_NEWS_URL = 'https://www.monsterhunter.com/ja/news'

# URL for Event Quests webpage
EVENT_QUEST_URL = 'https://info.monsterhunter.com/wilds/event-quest/en-asia/game/schedule'

# datetime.strftime formatting has different symbols being used between Windows and Linux for non-zero-padded items
# automatically switch between '#' for Windows and '-' for Linux
if sys.platform == 'linux':
	UNPADDED_SYMBOL = '-'
else:
	UNPADDED_SYMBOL = '#'

# URL string of the latest news image, used to identify each unique article
LATEST_NEWS_IMAGE = ''

# names and color codes for News categories
NEWS_MAPPING = {
	'cat_game': ['Game', 0x0D7EC4],
	'cat_media': ['Media', 0x019478],
	'cat_event': ['Event', 0x8C48AF],
	'cat_campaign': ['Campaign', 0xD77417],
	'cat_goods': ['Goods', 0xCF0707],
}

# color codes for Event Quest categories
# 1: Siege
# 2: Event
# 3: Challenge
# 4: Free Challenge
QUEST_COLOR_CODES = {
	'1': 0x0492C2,  # blue
	'2': 0xD8B863,  # yellow
	'3': 0x5DBB63,  # green
	'4': 0xDE3163,  # red
}

# dictionary of the available Discord statuses for the bot
# if activity (key) is meant to be a 'Streaming' activity, then corresponding value is a string URL
# otherwise corresponding value is the respective ActivityType
# available ActivityTypes: 0 is gaming (Playing), 1 is streaming (Streaming), 2 is listening (Listening to),
# 3 is watching (Watching), 4 is custom, 5 is competing (Competing in)
BOT_ACTIVITY_STATUSES = {
	"with Poogie": 0,
	"with Palicoes": 0,
	"with her Seikret": 0,
	"the Diva singing": 2,
	"Nata yapping away": 2,
	"the Wudwuds' shenanigans": 3,
	"barrel bowling": 5,
}
