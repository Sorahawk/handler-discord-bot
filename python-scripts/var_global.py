from sys import platform


### DISCORD ###

# ID of Discord server channel to send event quest notifications
QUEST_CHANNEL_ID = 1349006234375950337

# ID of Discord server channel to send news notifications
NEWS_CHANNEL_ID = 1356173681369415871

# quest channel object, to be initialised when the bot calls on_ready()
QUEST_CHANNEL = None

# news channel object, to be initialised when the bot calls on_ready()
NEWS_CHANNEL = None

# Discord server role name to ping for notifications
NOTIFY_ROLE_NAME = '<@&1097703521886941274>'


### MAIN ###

BOT_INSTANCE = None

# symbol to signify bot commands
BOT_COMMAND_PREFIX = '.'

# color codes for Event Quest categories
QUEST_COLOR_CODES = {
	'1': 0x0492C2,  # blue
	'2': 0xD8B863,  # yellow
	'3': 0xDE3163,  # red
	'4': 0x5DBB63,  # green
}

# names and color codes for News categories
NEWS_MAPPING = {
	'cat_game': ['Game', 0x0D7EC4],
	'cat_media': ['Media', 0x019478],
	'cat_event': ['Event', 0x8C48AF],
	'cat_campaign': ['Campaign', 0xD77417],
	'cat_goods': ['Goods', 0xCF0707],
}

# proxy URL to route web traffic through
PROXY_URL = 'http://gw.dataimpulse.com:823'

# URL for Event Quests webpage
EVENT_QUEST_URL = 'https://info.monsterhunter.com/wilds/event-quest/en-asia/game/schedule'

# URL for Japanese News webpage
JAPANESE_NEWS_URL = 'https://www.monsterhunter.com/ja/news'

# standard headers for HTTP requests
STANDARD_HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }

# datetime.strftime formatting has different symbols being used between Windows and Linux for non-zero-padded items
# automatically switch between '#' for Windows and '-' for Linux
if platform == 'linux':
	UNPADDED_SYMBOL = '-'
else:
	UNPADDED_SYMBOL = '#'

# URL string of the latest news image, used to identify each unique article
LATEST_NEWS_IMAGE = ''
