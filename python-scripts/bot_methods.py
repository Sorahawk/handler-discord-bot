from imports import *


# all bot methods below have to correspond to an item in BOT_COMMAND_LIST
# and must share the same name, followed by '_method'


# display weekly quests
async def quest_method(message, user_input, flag_presence):
	week_index = 0
	if 'next' in user_input.lower():
		week_index = 1
	elif 'latest' in user_input.lower():
		week_index = -1

	await display_weekly_quests(message.channel, week_index=week_index, display_all=flag_presence['all'])


# trigger bot self-update
async def update_method(message, user_input, flag_presence):
	if sys.platform != 'linux':
		return

	await message.channel.send('Popping into the tent for a bit!')

	# reset any potential changes to project folder, then pull latest code
	subprocess.run(f"cd {LINUX_ABSOLUTE_PATH} && git reset --hard HEAD && git clean -d -f && git pull", shell=True)

	# restart service
	subprocess.run(f"sudo systemctl restart {LINUX_SERVICE_NAME}", shell=True)
