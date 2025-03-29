from sys import platform


### DISCORD ###

# ID of default Discord server channel that will receive notifications
MAIN_CHANNEL_ID = 1349006234375950337

# main channel object, to be initialised when the bot calls on_ready()
MAIN_CHANNEL = None

# Discord server role name to ping for notifications
NOTIFY_ROLE_NAME = '<@&1097703521886941274>'


### MAIN ###

BOT_INSTANCE = None

# symbol to signify bot commands
BOT_COMMAND_PREFIX = '.'

# color codes for Embed messages
EMBED_COLOR_CODES = {
	'1': 0x0492C2,  # blue
	'2': 0xD8B863,  # yellow
	'3': 0xDE3163,  # red
	'4': 0x5DBB63,  # green
}

# URL for Event Quest webpage
EVENT_QUEST_URL = 'https://info.monsterhunter.com/wilds/event-quest/en-asia/game/schedule'

# standard headers for HTTP requests
STANDARD_HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }

# datetime.strftime formatting has different symbols being used between Windows and Linux for non-zero padded items
# automatically switch between '#' for Windows and '-' for Linux
if platform == 'linux':
	NONZERO_DATETIME_SYMBOL = '-'
else:
	NONZERO_DATETIME_SYMBOL = '#'
