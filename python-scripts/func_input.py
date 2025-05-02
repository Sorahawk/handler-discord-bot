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
		return f'{keyword}_method', sliced_input


# checks for presence of any command flags in user input
# returns a tuple containing:
# first, a dictionary of booleans indicating presence of command flags
# second, the user input stripped of flags
def check_flags(user_input):
	flag_presence = {}

	# insert surrounding whitespace so leading and trailing flags can still be detected
	user_input = f' {user_input} '

	for flag_key, flag in BOT_COMMAND_FLAGS.items():
		flag_presence[flag_key] = False
		flag = f' -{flag} '  # flag must be standalone with surrounding whitespace

		if flag in user_input.lower():
			flag_presence[flag_key] = True

	# remove all 'flags', a dash followed by a single letter, even if they are not valid
	all_flags = ' -[a-z] '

	# duplicate each whitespace within the input so that each present flag can be matched by the regex properly
	user_input = re.sub(all_flags, ' ', ' ' + user_input.replace(' ', '  ') + ' ', flags=re.IGNORECASE)

	# remove excess whitespace
	user_input = ' '.join(user_input.split())

	return flag_presence, user_input
