import global_constants

from secret_variables import *
from global_constants import *
from helper_functions import *

from discord.ext.tasks import loop
from discord import Activity, Client, Intents
from datetime import datetime, time, timedelta, timezone


# declare bot intents
# all() enables everything, including the privileged intents: presences, members and message_content
intents = Intents.all()

# initialise client
bot = Client(intents=intents)
global_constants.BOT_INSTANCE = bot


tz = timezone(timedelta(hours=8))  # UTC+8
@loop(time=time(hour=8, minute=1, tzinfo=tz))  # 8.01am SGT, but Discord seems to execute the task a few seconds before the minute actually occurs. In this case, also give the website a minute to update to the next week
async def display_weekly_quests():

	if datetime.now(tz).weekday() != 2:  # only continue on Wednesdays
		return

	greeting_msg = f"Greetings, Hunters! It's the start of a new week!"
	await global_constants.MAIN_CHANNEL.send(greeting_msg)
	await process_weekly_quests(global_constants.MAIN_CHANNEL)


@bot.event
async def on_message(message):
	prefix_length = len(BOT_COMMAND_PREFIX)  # prefix might not always be single character

	# ignore any messages if bot is not ready, messages sent from the bot itself, or messages that don't start with the command prefix
	if not bot.is_ready() or message.author == bot.user or message.content[:prefix_length] != BOT_COMMAND_PREFIX:
		return

	contents = message.content[prefix_length:].split()

	# quests command
	if contents[0].lower() == 'quests':
		week_index = 0

		# handle week_index optional parameter
		if len(contents) > 1:

			if contents[1].lstrip('-').isdigit():  # allow negative integers
				week_index = int(contents[1])

			elif contents[1].lower() == 'now':
				week_index = 0
			elif contents[1].lower() == 'next':
				week_index = 1
			elif contents[1].lower() == 'latest':
				week_index = -1

		await process_weekly_quests(message.channel, week_index=week_index)


@bot.event
async def on_ready():
	# on_ready() may be called more than once, typically whenever the bot momentarily loses connection to Discord 
	# check if this is first time bot is calling on_ready()
	if global_constants.MAIN_CHANNEL:
		return

	print(f"{bot.user} is online.\n")

	# initialise global main channel object
	global_constants.MAIN_CHANNEL = bot.get_channel(MAIN_CHANNEL_ID)

	# start tasks
	display_weekly_quests.start()

	# set activity status
	# available ActivityTypes: 0 is gaming (Playing), 1 is streaming (Streaming), 2 is listening (Listening to),
	# 3 is watching (Watching), 4 is custom, 5 is competing (Competing in)
	activity_status = Activity(type=2, name='Nata yapping away')
	await global_constants.BOT_INSTANCE.change_presence(activity=activity_status)


# start bot
bot.run(DISCORD_BOT_TOKEN)
