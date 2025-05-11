from imports import *


# checks for the latest info on Wilds
async def check_wilds_info():
	# retrieve webpage contents
	# main_webpage = await make_get_request(WILDS_MAIN_URL, use_proxy=True)
	# update_webpage = await make_get_request(WILDS_UPDATE_URL)
	# support_webpage = await make_get_request(WILDS_SUPPORT_URL, use_proxy=True)


	# TEMP
	with open('wilds_main.html', encoding='utf-8') as infile:
		main_webpage = '\n'.join(infile.readlines())
	with open('wilds_patch.html', encoding='utf-8') as infile:
		update_webpage = '\n'.join(infile.readlines())
	with open('wilds_support.html', encoding='utf-8') as infile:
		support_webpage = '\n'.join(infile.readlines())


	# process HTML data
	main_html = html.fromstring(main_webpage).find_class('ov-100')[0]
	update_html = html.fromstring(update_webpage)
	support_html = html.fromstring(support_webpage)

	# consolidate new info items across all types
	details_list = []
	details_list += check_wilds_news(main_html)
	details_list += check_wilds_notice(main_html)
	details_list += check_wilds_update(update_html)
	details_list += check_wilds_support(support_html)


	# TEMP
	print(var_global.LATEST_WILDS_IMAGE)
	print(var_global.LATEST_WILDS_NOTICE)
	print(var_global.LATEST_WILDS_UPDATE)
	print(var_global.LATEST_WILDS_SUPPORT)


	# generate a dictionary which maps each category to its index position in INFO_MAPPING
	order = {category: index for index, category in enumerate(INFO_MAPPING)}

	# sort new items primarily by date, then subsequently by type
	details_list = sorted(details_list, key=lambda item: (item["date"], order[item["category"]]))

	# iterate through new items, in correct order
	for details in details_list:
		await send_news_embed(details, var_global.INFO_CHANNEL)


# processes 'News' section of Wilds main page
def check_wilds_news(html_data):

	# consolidate current news items
	details_list = []
	first_run = not var_global.LATEST_WILDS_IMAGE
	item_list = html_data.find_class('news-container')[0].find_class('news-item')

	for item in item_list:
		image_link = urljoin(WILDS_MAIN_URL, item.xpath('div/p/img')[0].get('src'))

		# set latest news image on fresh startup
		if first_run:
			var_global.LATEST_WILDS_IMAGE.append(image_link)
			continue

		# break iteration once latest item is matched
		elif image_link in var_global.LATEST_WILDS_IMAGE:
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
		var_global.LATEST_WILDS_IMAGE += [details['image_link'] for details in details_list]

	return details_list


# processes 'Important Notice' section of Wilds main page
def check_wilds_notice(html_data):

	# skip if 'Important Notice' section is not present on webpage
	if not (item_list := html_data.find_class('ImportantNotice_list')):
		return item_list

	# consolidate current notices
	details_list = []
	first_run = not var_global.LATEST_WILDS_NOTICE

	for item in item_list[0].xpath('li/a'):
		# construct identifier string to 'mark' latest notice
		date = item.xpath('dl/dt')[0].text_content().strip()
		caption = ' '.join(item.xpath('dl/dd')[0].text_content().split())
		identifier = f"{date}|{caption}"

		# set latest identifier on fresh startup
		if first_run:
			var_global.LATEST_WILDS_NOTICE.append(identifier)
			continue

		# break iteration once latest item is matched
		elif identifier in var_global.LATEST_WILDS_NOTICE:
			break

		details = {
			'category': (category := 'notice'),
			'title_link': WILDS_MAIN_URL,
			'identifier': identifier
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
		var_global.LATEST_WILDS_NOTICE += [details['identifier'] for details in details_list]

	return details_list


# processes patch notes of Wilds update information page
def check_wilds_update(html_data):

	# consolidate current patch notes
	details_list = []
	first_run = not var_global.LATEST_WILDS_UPDATE
	item_list = html_data.find_class('latest_update')[0].xpath('li/a')

	for item in item_list:
		article_link = urljoin(WILDS_UPDATE_URL, item.get('href'))

		# set latest patch notes on fresh startup
		if first_run:
			var_global.LATEST_WILDS_UPDATE.append(article_link)
			continue

		# break iteration once latest item is matched
		elif article_link in var_global.LATEST_WILDS_UPDATE:
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
		var_global.LATEST_WILDS_UPDATE += [details['article_link'] for details in details_list]

	return details_list


# processes support articles of Wilds support page
def check_wilds_support(html_data):

	# generate reference dict containing article timings
	faq_data = json.loads(html_data.get_element_by_id('__NEXT_DATA__').text_content())['props']['pageProps']['faq_list']['faq_article_list']
	article_timings = {faq['slug']: datetime.fromtimestamp(faq['date']) for faq in faq_data}

	# consolidate current support articles
	details_list = []
	first_run = not var_global.LATEST_WILDS_SUPPORT
	item_list = html_data.find_class('Search_faqList___dcjt')[0].xpath('div/div/a')

	for item in item_list:
		article_link = urljoin(WILDS_SUPPORT_URL, item.get('href'))

		# set latest support article on fresh startup
		if first_run:
			var_global.LATEST_WILDS_SUPPORT.append(article_link)
			continue

		# break iteration once latest item is matched
		elif article_link in var_global.LATEST_WILDS_SUPPORT:
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
		var_global.LATEST_WILDS_SUPPORT += [details['article_link'] for details in details_list]

	return details_list
