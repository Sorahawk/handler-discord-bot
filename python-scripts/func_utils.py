from imports import *


# determines if user input contains any command
# if no command detected, returns None
# otherwise, returns a tuple containing:
# first, the name of the corresponding method of the bot command as a string to be called by eval()
# second, the user input stripped of command word
def check_command(user_input):
	# isolate first word
	keyword = user_input.split()[0].lower()

	if keyword in BOT_COMMAND_LIST:
		# remove command word from user input
		sliced_input = re.sub(keyword, '', user_input, flags=re.IGNORECASE).strip()
		return f"{keyword}_method", sliced_input


# checks for presence of any command flags in user input
# returns a tuple containing:
# first, a dictionary of booleans indicating presence of command flags
# second, the user input stripped of flags
def check_flags(user_input):
	# insert surrounding whitespace so leading and trailing flags can still be detected
	user_input = f" {user_input} "

	# generate flag presence dictionary
	flag_presence = {flag: True if f" -{letter} " in user_input.lower() else False for flag, letter in BOT_COMMAND_FLAGS.items()}

	# remove all 'flags', a dash followed by a single letter, even if they are not valid
	# each whitespace within input is duplicated so that all present flags can be matched by the regex properly
	user_input = re.sub(' -[a-z] ', ' ', ' ' + user_input.replace(' ', '  ') + ' ', flags=re.IGNORECASE)

	# remove excess whitespace
	user_input = ' '.join(user_input.split())

	return flag_presence, user_input


# returns a Discord File object
def generate_file(content, filename):
	return discord.File(io.StringIO(content), filename=filename)


# converts a datetime object into a formatted string to be used in identifier strings
def format_identifier_date(dt):
	return dt.strftime('%y%m%d')


# makes a GET request using globally-declared httpx.AsyncClient()
# usage of proxy required when hitting www.monsterhunter.com; VPN alone unable to bypass, unlike for info.monsterhunter.com
async def make_get_request(url, use_proxy=False, get_content=False):
	client = var_global.ASYNC_CLIENT_PROXY if use_proxy else var_global.ASYNC_CLIENT
	response = await client.get(url, headers=STANDARD_HEADERS)

	# check if CloudFront blocked the request, indicating that the VPN is inactive
	if 'error from cloudfront' in response.headers.get('X-Cache', '').lower():
		raise Exception('HTTP request blocked by CloudFront. Verify VPN connection is active.')

	return response.content if get_content else response.text


# obtains full traceback of given exception and outputs to specified channel
async def send_traceback(e, channel):
	full_trace = ''.join(traceback.format_exception(type(e), e, e.__traceback__))

	if len(full_trace) <= 2000:
		await channel.send(full_trace)
	else:
		await channel.send(e, file=generate_file(full_trace, 'traceback.txt'))
