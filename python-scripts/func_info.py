from imports import *


# checks for the latest info on Wilds
async def check_wilds_info():
	# retrieve webpage contents
	main_webpage = make_get_request(WILDS_MAIN_URL, use_proxy=True).text
	update_webpage = make_get_request(WILDS_UPDATE_URL).text
	support_webpage = make_get_request(WILDS_SUPPORT_URL, use_proxy=True).text

	# process HTML data
	main_html = html.fromstring(main_webpage)
	update_html = html.fromstring(update_webpage)
	support_html = html.fromstring(support_webpage)

	# consolidate new info items across all types
	details_list = []
	details_list += await check_wilds_news(main_html)
	details_list += await check_wilds_notice(main_html)
	details_list += await check_wilds_update(update_html)
	details_list += await check_wilds_support(support_html)

	# generate a dictionary which maps each category to its index position in INFO_MAPPING
	order = {category: index for index, category in enumerate(INFO_MAPPING)}

	# sort new items primarily by date, then subsequently by type
	details_list = sorted(details_list, key=lambda item: (item["date"], order[item["category"]]))

	# iterate through new items, in correct order
	for details in details_list:
		await send_news_embed(details, var_global.INFO_CHANNEL)


# processes 'News' section of Wilds main page
async def check_wilds_news(html_data):

	# consolidate current news items
	item_list = html_data.find_class('news-container')[0].find_class('news-item')
	details_list = []

	for item in item_list:
		image_link = urljoin(WILDS_MAIN_URL, item.xpath('div/p/img')[0].get('src'))

		# set latest news image on fresh startup
		if not var_global.LATEST_WILDS_IMAGE:
			var_global.LATEST_WILDS_IMAGE = image_link
			return []

		# break iteration once latest item is matched
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


# processes 'Important Notice' section of Wilds main page
async def check_wilds_notice(html_data):

	# extract 'Important Notice' section
	notice_block = html_data.get_element_by_id('ImportantNotice', None)

	# skip if 'Important Notice' section is not present on webpage
	if notice_block is None:
		var_global.LATEST_WILDS_NOTICE = []
		await var_global.INFO_CHANNEL.send('Important Notice section is not present on Wilds webpage.')
		return []

	# consolidate current notices
	item_list = notice_block.find_class('ImportantNotice_list')[0].xpath('li/a')
	details_list = []

	for item in item_list:

		# construct identifier string to 'mark' latest notice
		date = item.xpath('dl/dt')[0].text_content().strip()
		caption = ' '.join(item.xpath('dl/dd')[0].text_content().split())
		notice_identifier = f"{date} {caption}"

		# set latest notice identifier on fresh startup
		if not var_global.LATEST_WILDS_NOTICE:
			var_global.LATEST_WILDS_NOTICE = notice_identifier
			return []

		# break iteration once latest item is matched
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


# processes patch notes of Wilds update information page
async def check_wilds_update(html_data):

	# consolidate current patch notes
	item_list = html_data.find_class('latest_update')[0].xpath('li/a')
	details_list = []

	for item in item_list:
		article_link = urljoin(WILDS_UPDATE_URL, item.get('href'))

		# set latest patch notes on fresh startup
		if not var_global.LATEST_WILDS_UPDATE:
			var_global.LATEST_WILDS_UPDATE = article_link
			return []

		# break iteration once latest item is matched
		elif article_link == var_global.LATEST_WILDS_UPDATE:
			break

		details = {
			'category': (category := 'update'),
			'title_link': WILDS_UPDATE_URL,
			'article_link': article_link
		}

		# set title and color code
		details['title'], details['color_code'] = INFO_MAPPING[category]

		# set description
		version_number = ' '.join(item.find_class('latest_update_list_ver')[0].text_content().split())
		details['description'] = f"**[{version_number}]({article_link})**"

		# extract image if present
		if (image := item.find_class('latest_update_list_thumb')):
			details['image_link'] = urljoin(WILDS_UPDATE_URL, image[0].xpath('img')[0].get('src'))

		# extract release date
		# regex pattern to match a word (month), followed by 1-2 digits (day), an optional comma, then 4 digits (year)
		release_date = re.search(r'[a-zA-Z]+\s+\d{1,2},?\s+\d{4}', item.find_class('latest_update_list_date')[0].xpath('dd')[0].text_content().strip())
		release_date = datetime.strptime(release_date.group().replace(',', ''), '%B %d %Y')
		details['release_date'] = release_date

		# format date
		# set to release date if it has already passed, otherwise current date
		details['date'] = now if release_date > (now := datetime.now()) else release_date

		# extract patch description
		update_details = item.find_class('latest_update_list_detail')[0]

		if (header := update_details.xpath('dt')[0].text_content().strip()):
			details['contents_header'] = header

		details['contents'] = '\n'.join([f'• {line.text_content().strip()}' for line in update_details.xpath('dd')])

		# extract platforms
		details['platforms'] = ', '.join([p.text_content().strip() for p in item.find_class('latest_update_list_platform')[0].xpath('li')])
		
		details_list.append(details)

	# update tracking if new item appeared
	if details_list:
		var_global.LATEST_WILDS_UPDATE = details_list[0]['article_link']

	return details_list


# processes support articles of Wilds support page
async def check_wilds_support(html_data):

	# generate reference dict containing article timings
	faq_data = json.loads(html_data.get_element_by_id('__NEXT_DATA__').text_content())['props']['pageProps']['faq_list']['faq_article_list']
	article_timings = {faq['slug']: datetime.fromtimestamp(faq['date']) for faq in faq_data}

	# consolidate current support articles
	item_list = html_data.find_class('Search_faqList___dcjt')[0].xpath('div/div/a')
	details_list = []

	for item in item_list:
		article_link = urljoin(WILDS_SUPPORT_URL, item.get('href'))

		# set latest support article on fresh startup
		if not var_global.LATEST_WILDS_SUPPORT:
			var_global.LATEST_WILDS_SUPPORT = article_link
			return []

		# break iteration once latest item is matched
		elif article_link == var_global.LATEST_WILDS_SUPPORT:
			break

		details = {
			'category': (category := 'support'),
			'title_link': WILDS_SUPPORT_URL,
			'article_link': article_link,
			'date': article_timings[article_link.split('/')[-1]]
		}

		# set title and color code
		details['title'], details['color_code'] = INFO_MAPPING[category]

		# set description
		caption = item.xpath('div/p')[0].text_content().strip()
		details['description'] = f"[{caption}]({article_link})"

		# extract article category
		details['labels'] = ', '.join([cat.text_content().strip() for cat in item.find_class('Label_ca___ZPtj')[0].xpath('span')])

		# extract article platforms
		details['platforms'] = ', '.join([p.text_content().strip() for p in item.find_class('Label_pl__hNw2r')[0].xpath('span')])

		details_list.append(details)

	# update tracking if new item appeared
	if details_list:
		var_global.LATEST_WILDS_SUPPORT = details_list[0]['article_link']

	return details_list
