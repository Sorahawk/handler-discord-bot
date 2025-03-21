import io, requests

from global_constants import *

from lxml import html
from datetime import datetime
from discord import Embed, File


# returns a formatted embed message containing quest details
def create_quest_embed(quest_details):
	embed_msg = Embed(title=quest_details['title'], url=EVENT_QUEST_URL, color=EMBED_COLOR_CODE)
	embed_msg.add_field(name='Description', value=quest_details['description'], inline=False)

	embed_msg.add_field(name='Objective', value=quest_details['completion_conditions'], inline=True)
	embed_msg.add_field(name='Locale', value=quest_details['locales'], inline=True)
	embed_msg.add_field(name='Difficulty', value=quest_details['difficulty'], inline=True)

	# format dates
	input_format = '%m.%d.%Y %H:%M'
	output_format = '%#d %B, %I.%M %p'
	start_date = datetime.strptime(quest_details['start_date_and_time'], input_format).strftime(output_format)
	end_date = datetime.strptime(quest_details['end_date_and_time'], input_format).strftime(output_format)

	embed_msg.add_field(name='Start', value=start_date, inline=True)
	embed_msg.add_field(name='End', value=end_date, inline=True)
	embed_msg.add_field(name='\u200b', value='\u200b', inline=True)

	# Discord is unable to get image content on its own, possibly due to headers being rejected by MH website
	# Thus, need to get the image data to pass into Discord directly
	image_data = requests.get(quest_details['image_url'], headers=STANDARD_HEADERS).content
	image_file = File(io.BytesIO(image_data), filename="image.jpg")
	embed_msg.set_image(url="attachment://image.jpg")

	return embed_msg, image_file


# sends all quests within a specified week as embed messages
async def process_weekly_quests(channel, week_index=0):
	try:
		events_webpage = requests.get(EVENT_QUEST_URL, headers=STANDARD_HEADERS).text
		html_data = html.fromstring(events_webpage)
		date_ranges = html_data.get_element_by_id('tab_top').getparent().find_class('tab1')[0].xpath('li/p')

	except Exception as e:
		await channel.send(f"ERROR: {e}")
		await channel.send(f"html_data: {html_data}")
		return

	# get dates of specified week
	specified_range = date_ranges[week_index]

	specified_range.xpath('span')[0].drop_tree()  # drop the span elements to ignore the 'This/next week' text
	dates = specified_range.text_content().strip().split()

	# format start and end dates
	input_format = '%m.%d.%Y'
	output_format = '%#d %B'
	start_date = datetime.strptime(dates[0], input_format).strftime(output_format)
	end_date = datetime.strptime(dates[-1], input_format).strftime(output_format)

	# check if specified week has no quest info available yet i.e. Coming Soon
	quest_table = html_data.find_class('tableArea')[week_index]

	if quest_table.find_class('coming-quest'):
		no_info_msg = f"I'm still awaiting correspondence from the Guild regarding authorised hunts for the week of {start_date} to {end_date}.\n\nTry checking back again in a few days!"
		await channel.send(no_info_msg)
		return

	# display message containing start and end dates of specified week
	dates_msg = f"From **{start_date}** to **{end_date}**, the Guild has authorised the following hunts!\n\u200b"
	await channel.send(dates_msg)

	# display quests
	for quest in quest_table.xpath('table/tbody/tr'):
		details = {}

		details['image_url'] = quest.xpath('td/img')[0].get('src')
		details['difficulty'] = quest.find_class('level')[0].text_content()
		details['title'] = quest.find_class('title')[0].xpath('span')[0].text_content()
		details['description'] = quest.find_class('txt')[0].text_content()

		# strip any excess whitespace for the values above
		for key, value in details.items():
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

		embed_msg, image = create_quest_embed(details)
		await channel.send(embed=embed_msg, file=image)
