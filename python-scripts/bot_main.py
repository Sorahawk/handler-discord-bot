from imports import *


# declare bot intents
# all() enables everything, including the privileged intents: presences, members and message_content
intents = discord.Intents.all()

# initialise client
bot = discord.Client(intents=intents)
var_global.BOT_INSTANCE = bot


# automatically rotate bot's Discord status every 10 minutes
@loop(minutes=10)
async def task_rotate_status():
	activity, activity_type = random.choice(list(BOT_ACTIVITY_STATUSES.items()))

	if isinstance(activity_type, str):
		activity_status = discord.Streaming(url=activity_type, name=activity)
	else:
		activity_status = discord.Activity(type=activity_type, name=activity)

	await var_global.BOT_INSTANCE.change_presence(activity=activity_status)


# poll for news every hour
@loop(hours=1)
async def task_check_latest_news():
	await check_latest_news()


# poll for Wilds info every hour
@loop(hours=1)
async def task_check_wilds_info():
	await check_wilds_info()


# execute weekly quest update weekly every Wednesday at 8.01am SGT
# Discord seems to execute the task a few seconds before the minute actually occurs.
# in this case, also give the website a minute to update to the next week
tz = timezone(timedelta(hours=8))  # UTC+8
@loop(time=time(hour=8, minute=1, tzinfo=tz))
async def task_display_weekly_quests():

	if datetime.now(tz).weekday() != 2:  # only execute on Wednesdays
		return

	greeting_msg = f"Greetings, Hunters! It's the start of a new week!"
	await var_global.QUEST_CHANNEL.send(greeting_msg)
	await display_weekly_quests(var_global.QUEST_CHANNEL, display_all=True)


@bot.event
async def on_ready():
	# on_ready() may be called more than once, typically whenever the bot momentarily loses connection to Discord 
	# check if this is first time bot is calling on_ready()
	if var_global.QUEST_CHANNEL:
		return

	print(f"{bot.user} is online.\n")

	# initialise global channel objects
	var_global.NEWS_CHANNEL = bot.get_channel(NEWS_CHANNEL_ID)
	var_global.INFO_CHANNEL = bot.get_channel(INFO_CHANNEL_ID)
	var_global.QUEST_CHANNEL = bot.get_channel(QUEST_CHANNEL_ID)

	# start tasks
	task_rotate_status.start()
	task_check_wilds_info.start()
	task_check_latest_news.start()
	task_display_weekly_quests.start()


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

	# check for any valid command if the message starts with the prefix symbol
	result = check_command(message.content[prefix_length:])
	if not result:
		return

	command_method, user_input = result[0], result[1]

	# check for presence of any command flags
	# in the process also removes any excess whitespace
	flag_presence, user_input = check_flags(user_input)
	await eval(command_method)(message, user_input, flag_presence)


# start bot
bot.run(DISCORD_BOT_TOKEN)
