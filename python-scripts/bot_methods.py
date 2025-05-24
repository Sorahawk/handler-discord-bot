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


# display current state of article feeds
async def status_method(message, user_input, flag_presence):
	status_list = [
		"WILDS_NOTICE_LIST",
		"WILDS_UPDATE_LIST",
		"WILDS_SUPPORT_LIST",
		"WILDS_NEWS_LIST",
		"MH_NEWS_LIST",
	]

	status_log = '\n\n'.join(f"{name}: {json.dumps(getattr(var_global, name), indent=4)}" for name in status_list)
	await message.channel.send(file=generate_file(status_log, 'status_log.txt'))


# start/stop VPN connection on VM
async def vpn_method(message, user_input, flag_presence):
	if sys.platform != 'linux':
		return

	# start/stop VPN service
	action_messages = {
		'start': 'Ghillie Mantle equipped. Shhh, quietly now...',
		'stop': 'Ghillie Mantle unequipped. Be careful!',
	}

	for action, string_message in action_messages.items():
		if action in user_input.lower():
			await message.channel.send(string_message)
			return subprocess.run(['sudo', 'systemctl', action, VPN_SERVICE])


# trigger bot self-update
async def update_method(message, user_input, flag_presence):
	if sys.platform != 'linux':
		return

	if 'now' not in user_input.lower():
		# poll sites before restarting
		await safe_execute(check_wilds_info, var_global.INFO_CHANNEL)
		await safe_execute(check_latest_news, var_global.NEWS_CHANNEL)
		await status_method(message, user_input, flag_presence)

	await message.channel.send('Popping into the tent for a bit!')

	# reset any potential changes to project folder, then pull latest code
	subprocess.run(f"cd {LINUX_ABSOLUTE_PATH} && git reset --hard HEAD && git clean -d -f && git pull", shell=True)

	# restart service
	subprocess.run(['sudo', 'systemctl', 'restart', LINUX_SERVICE_NAME])
