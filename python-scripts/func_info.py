from imports import *


# checks for the latest info on Wilds
async def check_wilds_info():
	# retrieve webpage contents
	main_webpage = make_get_request(WILDS_MAIN_URL, use_proxy=True).text
	update_webpage = make_get_request(WILDS_UPDATE_URL).text
	support_webpage = make_get_request(WILDS_SUPPORT_URL, use_proxy=True).text

	# process HTML data
	html_data_main = html.fromstring(main_webpage)

	# consolidate new info items across all types
	details_list = []
	details_list += await process_wilds_news(html_data_main)
	details_list += await process_wilds_notice(html_data_main)

	# generate a dictionary which maps each category to its index position in INFO_MAPPING
	order = {category: index for index, category in enumerate(INFO_MAPPING)}

	# sort new items primarily by date, then subsequently by type
	details_list = sorted(details_list, key=lambda item: (item["date"], order[item["category"]]))

	# iterate through new items, in correct order
	for details in details_list:
		await send_news_embed(details, var_global.INFO_CHANNEL)


# processes 'News' section of Wilds main page
async def process_wilds_news(html_data):
	try:
		# check for Wilds news
		news_list = html_data.find_class('news-container')[0].find_class('news-item')
		details_list = []

		for item in news_list:
			image_link = urljoin(WILDS_MAIN_URL, item.xpath('div/p/img')[0].get('src'))

			# set latest news image on fresh startup
			if not var_global.LATEST_WILDS_IMAGE:
				var_global.LATEST_WILDS_IMAGE = image_link
				break

			# break iteration once latest news image is matched
			elif image_link == var_global.LATEST_WILDS_IMAGE:
				break

			details = {
				'category': (category := 'news'),
				'title_link': WILDS_MAIN_URL,
				'image_link': image_link
			}

			# set title and color code
			details['title'], details['color_code'] = INFO_MAPPING[category]

			# set description
			caption = ' '.join(item.find_class('news-item__text')[0].text_content().split())
			article_link = urljoin(WILDS_MAIN_URL, item.get('href'))
			details['description'] = f"[{caption}]({article_link})"

			# format date
			date = item.find_class('news-item__ymd')[0].text_content().strip()
			input_format = '%Y.%m.%d'
			details['date'] = datetime.strptime(date, input_format)

			details_list.append(details)

		# update tracking if new item appeared
		if details_list:
			var_global.LATEST_WILDS_IMAGE = details_list[0]['image_link']

		return details_list

	except Exception as e:
		await send_traceback(e, var_global.INFO_CHANNEL)


# processes 'Important Notice' section of Wilds main page
async def process_wilds_notice(html_data):
	try:
		# extract 'Important Notice' section
		notice_block = html_data.get_element_by_id('ImportantNotice', None)

		# skip if 'Important Notice' section is not present on webpage
		if notice_block is None:
			var_global.LATEST_WILDS_NOTICE = []
			await var_global.INFO_CHANNEL.send('Important Notice section is not present on Wilds webpage.')
			return

		# consolidate current notices
		notice_list = notice_block.find_class('ImportantNotice_list')[0].xpath('li/a')
		details_list = []

		for item in notice_list:

			# construct identifier string to 'mark' latest notice
			date = item.xpath('dl/dt')[0].text_content().strip()
			caption = ' '.join(item.xpath('dl/dd')[0].text_content().split())
			notice_identifier = f"{date} {caption}"

			# set latest notice identifier on fresh startup
			if not var_global.LATEST_WILDS_NOTICE:
				var_global.LATEST_WILDS_NOTICE = notice_identifier
				break

			# break iteration once latest notice is matched
			elif notice_identifier == var_global.LATEST_WILDS_NOTICE:
				break

			details = {
				'category': (category := 'notice'),
				'title_link': WILDS_MAIN_URL,
				'notice_identifier': notice_identifier
			}

			# set title and color code
			details['title'], details['color_code'] = INFO_MAPPING[category]

			# set description
			article_link = urljoin(WILDS_MAIN_URL, item.get('href'))
			details['description'] = f"[{caption}]({article_link})"

			# format date
			input_format = '%B %d, %Y'
			details['date'] = datetime.strptime(date, input_format)

			details_list.append(details)

		# update tracking if new item appeared
		if details_list:
			var_global.LATEST_WILDS_NOTICE = details_list[0]['notice_identifier']

		return details_list

	except Exception as e:
		await send_traceback(e, var_global.INFO_CHANNEL)


# processes patch notes of Wilds update information page
async def process_wilds_notice(html_data):
	pass
