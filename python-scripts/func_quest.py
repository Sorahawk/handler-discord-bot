from imports import *


# sends all quests within a specified week as embed messages
async def display_weekly_quests(channel, week_index=0, display_all=False):
	# retrieve webpage contents
	events_webpage = await make_get_request(EVENT_QUEST_URL)

	# process HTML data
	html_data = html.fromstring(events_webpage)
	date_ranges = html_data.get_element_by_id('tab_top').getparent().find_class('tab1')[0].xpath('li/p')

	# get dates of specified week
	(specified_range := date_ranges[week_index]).xpath('span')[0].drop_tree()  # drop the span elements to ignore the 'This/next week' text
	dates = specified_range.text_content().strip().split()

	# format start and end dates
	input_format = '%m.%d.%Y'
	output_format = f'%{UNPADDED_SYMBOL}d %B'
	start_date = datetime.strptime(dates[0], input_format).strftime(output_format)
	end_date = datetime.strptime(dates[-1], input_format).strftime(output_format)

	# check if specified week has no quest info available yet i.e. Coming Soon
	quest_table = html_data.find_class('tableArea')[week_index]

	if quest_table.find_class('coming-quest'):
		no_info_msg = f"I'm still awaiting correspondence from the Guild regarding authorised hunts for the week of **{start_date}** to **{end_date}**.\n\nTry checking back again in a few days!"
		await channel.send(no_info_msg)
		return

	# display message containing start and end dates of specified week
	if display_all:
		await channel.send(f"From **{start_date}** to **{end_date}**, the Guild has authorised all of the following hunts!")
	else:
		await channel.send(f"The Guild has authorised these new hunts from **{start_date}** to **{end_date}**!")

	# display quests
	for quest_category in quest_table.xpath('table'):

		# get category type (integer) and name
		# there seems to be 1 to 4 based on website data
		table_int = quest_category.get('class')[-1]
		category_name = quest_table.find_class(f'tableTitle type{table_int}')[0].text_content().strip()[:-1]

		for quest in quest_category.xpath('tbody/tr'):

			# check if quest should be displayed
			if not (is_new := quest.find_class('label_new')) and not display_all:
				continue

			details = {
				'category_name': category_name,
				'color_code': QUEST_COLOR_CODES[table_int],
				'image_link': quest.xpath('td/img')[0].get('src'),
				'difficulty': quest.find_class('level')[0].text_content(),
				'title': quest.find_class('title')[0].xpath('span')[0].text_content()
			}

			# append [NEW] label if quest is new
			if is_new:
				details['title'] += ' [NEW]'

			# insert '\n' to any <br> tags within the description text element
			for br in (description := quest.find_class('txt')[0]).xpath('br'):
				br.text = '\n'
			details['description'] = description.text_content()

			# strip any excess whitespace for the values above
			for key, value in details.items():
				if isinstance(value, str):
					details[key] = ' '.join(value.split())

			# retrieve details under 'Quest Info'
			for entry in quest.find_class('overview')[0].xpath('ul/li'):

				key = entry.find_class('overview_dt')[0].text_content()
				value = entry.find_class('overview_dd')[0].text_content()
				
				# remove any excess whitespace for both keys and values
				key = ' '.join(key.split())
				value = ' '.join(value.split())

				# lower the key names and replace whitespace with underscore
				key = key.lower().replace(' ', '_')

				# remove only the preceding colon, but cannot use .replace() because the Start/End quest timings contain colons as well
				value = value[1:]

				details[key] = value

			await send_quest_embed(details, channel)
