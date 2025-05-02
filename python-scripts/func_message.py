from imports import *


# determines if user input contains any command
# if no command detected, returns None
# otherwise, returns a tuple containing:
# first, the name of the corresponding method of the bot command as a string to be called by eval()
# second, the user input stripped of command word
def check_command(user_input):
	lowered_input = user_input.lower() + ' '

	for command_name in BOT_COMMAND_LIST:
		command = command_name + ' '

		if lowered_input.startswith(command):
			# slice command word out of input string
			user_input = user_input[len(command):]

			return f'{command_name}_method', user_input


# checks for presence of any command flags in user input
# returns a tuple containing:
# first, a dictionary of booleans indicating presence of command flags
# second, the user input stripped of flags
def check_flags(user_input):
	flag_presence = {}

	# insert surrounding whitespace so leading and trailing flags can be detected
	user_input = f' {user_input} '

	for flag_key, flag in BOT_COMMAND_FLAGS.items():
		flag_presence[flag_key] = False
		flag = f' -{flag} '  # flag must be standalone with surrounding whitespace

		if flag in user_input.lower():
			flag_presence[flag_key] = True

		# if flag not in query, replacing won't affect the string
		user_input = user_input.replace(flag.lower(), ' ').replace(flag.upper(), ' ')

	# remove any other 'flags', a dash followed by a single letter, even if they are not valid
	other_flags = '-[a-zA-Z] '
	user_input = re.sub(other_flags, ' ', user_input + ' ')

	# remove any excess whitespace
	user_input = ' '.join(user_input.split())

	return flag_presence, user_input
