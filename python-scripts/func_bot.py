from func_embed import *


# checks for the latest news articles
async def check_latest_news():
	try:
		# retrieve webpage contents via proxy
		# `www` subdomain seems to be stricter than `info`
		news_webpage = make_get_request(JAPANESE_NEWS_URL, use_proxy=True).text

		# process HTML data
		html_data = html.fromstring(news_webpage)
		news_list = html_data.find_class('mhNews_list')[0]

	except Exception as e:
		await var_global.NEWS_CHANNEL.send(f"ERROR in `check_latest_news`: {e}")
		await var_global.NEWS_CHANNEL.send(f"```{news_webpage}```")
		return

	latest_image_link = news_list[0].xpath('li/figure/img')[0].get('src')

	# set latest article
	if not var_global.LATEST_NEWS_IMAGE:
		var_global.LATEST_NEWS_IMAGE = latest_image_link

	# new articles detected
	elif latest_image_link != var_global.LATEST_NEWS_IMAGE:
		embed_list = []
		translator = googletrans.Translator()

		for article in news_list:
			image_link = article.xpath('li/figure/img')[0].get('src')

			# break iteration once latest registered article is matched
			if image_link == var_global.LATEST_NEWS_IMAGE:
				break

			details = { 'image_link': image_link }

			details['article_link'] = article.get('href')
			details['date'] = article.find_class('date')[0].text_content().strip()

			# extract specific category
			category_class = article.find_class('category')[0].get('class').replace('category', '').strip()
			details['category'], details['color_code'] = NEWS_MAPPING[category_class]

			# translate Japanese text to English
			caption_jap = article.find_class('text')[0].text_content().strip()
			details['caption_jap'] = caption_jap
			details['caption_eng'] = (await translator.translate(caption_jap, src='ja', dest='en')).text

			# create Embed message
			embed_msg, image_file = create_news_embed(details)
			embed_list.append((embed_msg, image_file, image_link))

		# send embeds in correct order (earliest to latest)
		for article_embed in embed_list[::-1]:
			await var_global.NEWS_CHANNEL.send(embed=article_embed[0], file=article_embed[1])

			# update tracking of latest article sent
			var_global.LATEST_NEWS_IMAGE = article_embed[-1]


# sends all quests within a specified week as embed messages
async def display_weekly_quests(channel, week_index=0):
	try:
		# retrieve webpage contents
		events_webpage = make_get_request(EVENT_QUEST_URL).text

		# process HTML data
		html_data = html.fromstring(events_webpage)
		date_ranges = html_data.get_element_by_id('tab_top').getparent().find_class('tab1')[0].xpath('li/p')

	except Exception as e:
		await channel.send(f"ERROR in `display_weekly_quests`: {e}")
		await channel.send(f"```{events_webpage}```")
		return

	# get dates of specified week
	specified_range = date_ranges[week_index]

	specified_range.xpath('span')[0].drop_tree()  # drop the span elements to ignore the 'This/next week' text
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
	dates_msg = f"From **{start_date}** to **{end_date}**, the Guild has authorised the following hunts!\n\u200b"
	await channel.send(dates_msg)

	# display quests
	for quest_category in quest_table.xpath('table'):

		# get category type (integer) and name
		# there seems to be 1 to 4 based on website data
		table_int = quest_category.get('class')[-1]
		category_name = quest_table.find_class(f'tableTitle type{table_int}')[0].text_content().strip()[:-1]

		for quest in quest_category.xpath('tbody/tr'):
			details = {
				'category_name': category_name,
				'color_code': QUEST_COLOR_CODES[table_int]
			}

			details['image_url'] = quest.xpath('td/img')[0].get('src')
			details['difficulty'] = quest.find_class('level')[0].text_content()
			details['title'] = quest.find_class('title')[0].xpath('span')[0].text_content()

			# insert '\n' to any <br> tags within the description text element
			description = quest.find_class('txt')[0]
			for br in description.xpath('br'):
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

			embed_msg, image = create_quest_embed(details)
			await channel.send(embed=embed_msg, file=image)
