from imports import *


# checks for the latest info on Wilds
async def check_wilds_info():

	# retrieve webpage contents
	main_webpage = await make_get_request(WILDS_MAIN_URL)
	update_webpage = await make_get_request(WILDS_UPDATE_URL, ignore_cloudfront=True)
	support_webpage = await make_get_request(WILDS_SUPPORT_URL)

	# process HTML data
	main_html = html.fromstring(main_webpage).find_class('ov-100')[0]  # restrict the data because there are two ImportantNotices in the full HTML
	update_html = html.fromstring(update_webpage)
	support_html = html.fromstring(support_webpage)

	# consolidate new info items across all types
	details_list = []
	details_list += check_wilds_news(main_html)
	details_list += check_wilds_notice(main_html)
	details_list += check_wilds_update(update_html)
	details_list += check_wilds_support(support_html)

	# generate a dictionary which maps each category to its index position in INFO_MAPPING
	order = { category: index for index, category in enumerate(INFO_MAPPING) }

	# sort new items primarily by date, then subsequently by type
	details_list = sorted(details_list, key=lambda item: (item["date"], order[item["category"]]))

	# iterate through new items, in correct order
	for details in details_list:
		await send_news_embed(details, var_global.INFO_CHANNEL)


# processes 'News' section of Wilds main page
def check_wilds_news(html_data):
	details_list = []
	first_run = not var_global.WILDS_NEWS_LIST

	item_list = html_data.find_class('news-container')[0].find_class('news-item')
	for item in item_list:

		# format date
		date = item.find_class('news-item__ymd')[0].text_content().strip()
		dt = datetime.strptime(date, '%Y.%m.%d')

		# construct identifier string
		formatted_date = format_identifier_date(dt)
		image_link = urljoin(WILDS_MAIN_URL, item.xpath('div/p/img')[0].get('src'))
		identifier = f"{formatted_date}|{image_link}"

		# break iteration once any registered item is matched
		if identifier in var_global.WILDS_NEWS_LIST:
			break

		# register new item to list
		if first_run:
			var_global.WILDS_NEWS_LIST.append(identifier)
			continue
		else:
			var_global.WILDS_NEWS_LIST.insert(0, identifier)

		details = {
			'category': (category := 'news'),
			'title_link': WILDS_MAIN_URL,
			'date': dt,
			'image_link': image_link
		}

		# set title and color code
		details['title'], details['color_code'] = INFO_MAPPING[category]

		# set description
		caption = ' '.join(item.find_class('news-item__text')[0].text_content().split())
		article_link = urljoin(WILDS_MAIN_URL, item.get('href'))
		details['description'] = f"[{caption}]({article_link})"

		details_list.append(details)

	return details_list


# processes 'Important Notice' section of Wilds main page
def check_wilds_notice(html_data):
	details_list = []
	first_run = not var_global.WILDS_NOTICE_LIST

	# skip if 'Important Notice' section is not present on webpage
	if not (item_list := html_data.find_class('ImportantNotice_list')):
		if first_run:
			# insert a value into the list so first_run will be False in subsequent runs
			var_global.WILDS_NOTICE_LIST.append('')

		return item_list

	for item in item_list[0].xpath('li/a | li/div'):

		# format date
		date = item.xpath('dl/dt')[0].text_content().strip()
		dt = datetime.strptime(date, '%B %d, %Y')

		# construct identifier string
		formatted_date = format_identifier_date(dt)
		caption = ' '.join(item.xpath('dl/dd')[0].text_content().split())
		identifier = f"{formatted_date}|{caption}"

		# break iteration once any registered item is matched
		if identifier in var_global.WILDS_NOTICE_LIST:
			break

		# register new item to list
		if first_run:
			var_global.WILDS_NOTICE_LIST.append(identifier)
			continue
		else:
			var_global.WILDS_NOTICE_LIST.insert(0, identifier)

		details = {
			'category': (category := 'notice'),
			'title_link': WILDS_MAIN_URL,
			'date': dt
		}

		# set title and color code
		details['title'], details['color_code'] = INFO_MAPPING[category]

		# set description
		article_link = urljoin(WILDS_MAIN_URL, item.get('href'))
		if not article_link:  # set article link to main page if notice doesn't redirect to a separate page
			article_link = details['title_link']

		details['description'] = f"[{caption}]({article_link})"

		details_list.append(details)

	return details_list


# processes patch notes of Wilds update information page
def check_wilds_update(html_data):
	details_list = []
	first_run = not var_global.WILDS_UPDATE_LIST

	item_list = html_data.find_class('latest_update')[0].xpath('li/a')
	for item in item_list:
		article_link = urljoin(WILDS_UPDATE_URL, item.get('href'))

		# break iteration once any registered item is matched
		if article_link in var_global.WILDS_UPDATE_LIST:
			break

		# register new item to list
		if first_run:
			var_global.WILDS_UPDATE_LIST.append(article_link)
			continue
		else:
			var_global.WILDS_UPDATE_LIST.insert(0, article_link)

		details = {
			'category': (category := 'update'),
			'title_link': WILDS_UPDATE_URL
		}

		# set title and color code
		details['title'], details['color_code'] = INFO_MAPPING[category]

		# set description
		version_number = ' '.join(item.find_class('latest_update_list_ver')[0].text_content().split())
		details['description'] = f"**[{version_number}]({article_link})**"

		# format date

		## regex pattern to match a word (month), followed by 1-2 digits (day), an optional comma, then 4 digits (year)
		release_date = re.search(r'[a-zA-Z]+\s+\d{1,2},?\s+\d{4}', item.find_class('latest_update_list_date')[0].xpath('dd')[0].text_content().strip())
		release_date = datetime.strptime(release_date.group().replace(',', ''), '%B %d %Y')
		details['release_date'] = release_date

		## set embed date to release date if it has already passed, otherwise current date
		details['date'] = now if release_date > (now := datetime.now()) else release_date

		# extract image if present
		if (image := item.find_class('latest_update_list_thumb')):
			details['image_link'] = urljoin(WILDS_UPDATE_URL, image[0].xpath('img')[0].get('src'))

		# extract patch description
		update_details = item.find_class('latest_update_list_detail')[0]

		if (header := update_details.xpath('dt')[0].text_content().strip()):
			details['contents_header'] = header

		details['contents'] = '\n'.join([f"• {line.text_content().strip()}" for line in update_details.xpath('dd/ul/li')])

		# extract platforms
		details['platforms'] = ', '.join([p.text_content().strip() for p in item.find_class('latest_update_list_platform')[0].xpath('li')])
		
		details_list.append(details)

	return details_list


# processes support articles of Wilds support page
def check_wilds_support(html_data):
	details_list = []
	first_run = not var_global.WILDS_SUPPORT_LIST

	# generate reference dict containing article timings
	faq_data = json.loads(html_data.get_element_by_id('__NEXT_DATA__').text_content())['props']['pageProps']['faq_list']['faq_article_list']
	article_timings = { faq['slug']: datetime.fromtimestamp(faq['date']) for faq in faq_data }

	item_list = html_data.find_class('Search_faqList___dcjt')[0].xpath('div/div/a')
	for item in item_list:
		article_link = urljoin(WILDS_SUPPORT_URL, item.get('href'))

		# break iteration once any registered item is matched
		if article_link in var_global.WILDS_SUPPORT_LIST:
			break

		# register new item to list
		if first_run:
			var_global.WILDS_SUPPORT_LIST.append(article_link)
			continue
		else:
			var_global.WILDS_SUPPORT_LIST.insert(0, article_link)

		details = {
			'category': (category := 'support'),
			'title_link': WILDS_SUPPORT_URL
		}

		# set title and color code
		details['title'], details['color_code'] = INFO_MAPPING[category]

		# set description
		caption = item.xpath('div/p')[0].text_content().strip()
		details['description'] = f"[{caption}]({article_link})"

		# format date
		article_id = article_link.split('/')[-1]
		details['date'] = article_timings[article_id]

		# extract article categories and platforms
		def extract_labels(class_name):
			return ', '.join([label.text_content().strip() for label in item.find_class(class_name)[0].xpath('span')])

		details['issue_cat'] = extract_labels('Label_ca___ZPtj')
		details['platforms'] = extract_labels('Label_pl__hNw2r')

		details_list.append(details)

	return details_list
