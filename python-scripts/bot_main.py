from func_all import *


# declare bot intents
# all() enables everything, including the privileged intents: presences, members and message_content
intents = discord.Intents.all()

# initialise client
bot = discord.Client(intents=intents)
var_global.BOT_INSTANCE = bot


@loop(hours=1)
async def task_check_latest_news():
	await check_latest_news()


tz = timezone(timedelta(hours=8))  # UTC+8
@loop(time=time(hour=8, minute=1, tzinfo=tz))  # 8.01am SGT, but Discord seems to execute the task a few seconds before the minute actually occurs. In this case, also give the website a minute to update to the next week
async def task_display_weekly_quests():

	if datetime.now(tz).weekday() != 2:  # only continue on Wednesdays
		return

	greeting_msg = f"Greetings, Hunters! It's the start of a new week!"
	await var_global.QUEST_CHANNEL.send(greeting_msg)
	await display_weekly_quests(var_global.QUEST_CHANNEL)


@bot.event
async def on_message(message):
	prefix_length = len(BOT_COMMAND_PREFIX)  # prefix might not always be single character

	# ignore any messages if bot is not ready or messages sent from the bot itself
	if not bot.is_ready() or message.author == bot.user:
		return

	# delete any user messages from the quest announcements channel to keep it clean
	if message.channel.id == var_global.QUEST_CHANNEL.id:
		await message.delete()
		return

	# ignore messages that don't start with the command prefix
	if message.content[:prefix_length] != BOT_COMMAND_PREFIX:
		return

	# process commands
	contents = message.content[prefix_length:].lower().split()

	# quests command
	if contents[0] in ['quest', 'quests']:
		week_index = 0

		# handle optional parameter
		if len(contents) > 1:
			keyword = contents[1]

			if keyword == 'now':
				week_index = 0
			elif keyword == 'next':
				week_index = 1
			elif keyword == 'latest':
				week_index = -1

		await display_weekly_quests(message.channel, week_index=week_index)


@bot.event
async def on_ready():

	# set activity status
	# available ActivityTypes: 0 is gaming (Playing), 1 is streaming (Streaming), 2 is listening (Listening to),
	# 3 is watching (Watching), 4 is custom, 5 is competing (Competing in)
	activity_status = discord.Activity(type=2, name='Nata yapping away')
	await var_global.BOT_INSTANCE.change_presence(activity=activity_status)

	# on_ready() may be called more than once, typically whenever the bot momentarily loses connection to Discord 
	# check if this is first time bot is calling on_ready()
	if var_global.QUEST_CHANNEL:
		return

	print(f"{bot.user} is online.\n")

	# initialise global channel objects
	var_global.QUEST_CHANNEL = bot.get_channel(QUEST_CHANNEL_ID)
	var_global.NEWS_CHANNEL = bot.get_channel(NEWS_CHANNEL_ID)

	# start tasks
	task_check_latest_news.start()
	task_display_weekly_quests.start()


# start bot
bot.run(DISCORD_BOT_TOKEN)
