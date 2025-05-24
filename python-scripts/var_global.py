import sys


### LINUX ###

# absolute path to the project folder on the Linux cloud instance
# cannot use os.getcwd() because systemd service runs the script from root directory
LINUX_ABSOLUTE_PATH = '/home/ubuntu/handler-bot/python-scripts'

# name of the bot service running on the Linux cloud instance
LINUX_SERVICE_NAME = 'handler-bot.service'



### INIT ###

QUEST_CHANNEL = None
NEWS_CHANNEL = None
INFO_CHANNEL = None

ASYNC_CLIENT = None
ASYNC_CLIENT_PROXY = None



### DISCORD ###

# ID of Discord server channel to send event quest notifications
QUEST_CHANNEL_ID = 1349006234375950337

# ID of Discord server channel to send news notifications
NEWS_CHANNEL_ID = 1356173681369415871

# ID of Discord server channel to send Wilds info notifications
INFO_CHANNEL_ID = 1365653663238066207



### MAIN ###

# datetime.strftime formatting has different symbols being used between Windows and Linux for non-zero-padded items
# automatically switch between '#' for Windows and '-' for Linux
if sys.platform == 'linux':
	UNPADDED_SYMBOL = '-'
else:
	UNPADDED_SYMBOL = '#'

# symbol to signify bot commands
BOT_COMMAND_PREFIX = '.'

# list of bot commands
BOT_COMMAND_LIST = ['quest', 'status', 'update', 'vpn']

# dictionary of command flags
# each flag can only be a single letter
BOT_COMMAND_FLAGS = { 'all': 'a' }


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



### NETWORK ###

# name of VPN service
VPN_SERVICE = 'openvpn-client@surfshark-sg-udp.service'

# proxy URL to route web traffic through
PROXY_URL = 'http://gw.dataimpulse.com:823'

# standard headers for HTTP requests
STANDARD_HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }



### QUEST ###

# URL for Event Quests webpage
EVENT_QUEST_URL = 'https://info.monsterhunter.com/wilds/event-quest/en-asia/game/schedule'


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



### NEWS ###

# URL for Japanese News webpage
JAPANESE_NEWS_URL = 'https://www.monsterhunter.com/ja/news/'

# list of MH news articles; identifier is "YYMMDD|IMAGE_LINK"
MH_NEWS_LIST = []


# names and color codes for News categories
NEWS_MAPPING = {
	'cat_game': ['Game', 0x0D7EC4],
	'cat_event': ['Event', 0x8C48AF],
	'cat_goods': ['Goods', 0xCF0707],
	'cat_media': ['Media', 0x019478],
	'cat_campaign': ['Campaign', 0xD77417],
}



### INFO ###

# URL for Wilds main webpage
WILDS_MAIN_URL = 'https://www.monsterhunter.com/wilds/en-asia/'

# URL for Wilds patch notes webpage
WILDS_UPDATE_URL = 'https://info.monsterhunter.com/wilds/update/en-asia/'

# URL for Wilds support articles webpage
WILDS_SUPPORT_URL = 'https://www.monsterhunter.com/support/wilds/en/faq/search/category/_/platform/_/keyword/_/tag/_/order/modified/1'

# list of Wilds news articles; identifier is "YYMMDD|IMAGE_LINK"
WILDS_NEWS_LIST = []

# list of 'Important Notices' on Wilds main page; identifier is "YYMMDD|CAPTION"
WILDS_NOTICE_LIST = []

# list of Wilds patch notes; identifier is ARTICLE_LINK
WILDS_UPDATE_LIST = []

# list of Wilds support articles; identifier is ARTICLE_LINK
WILDS_SUPPORT_LIST = []


# names and color codes for Info categories
INFO_MAPPING = {
	'news': ['Game News', 0xD8B863],  # yellow
	'update': ['Update Information', 0x0492C2],  # blue
	'notice': ['Important Notice', 0xDE3163],  # red
	'support': ['Support Article', 0x5DBB63],  # green
}
