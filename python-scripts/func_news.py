from imports import *


# checks for the latest news article s
async def check_latest_news():

	# retrieve webpage contents via proxy because `www` subdomain seems to be stricter than `info`
	news_webpage = await make_get_request(JAPANESE_NEWS_URL, use_proxy=True)
	html_data = html.fromstring(news_webpage)

	details_list = []
	first_run = not var_global.MH_NEWS_LIST
	translator = googletrans.Translator()

	news_list = html_data.find_class('mhNews_list')[0]
	for article in news_list:

		# format date
		date = article.find_class('date')[0].text_content().strip()
		details['date'] = datetime.strptime(date, '%Y.%m.%d')

		# construct identifier string
		image_link = article.xpath('li/figure/img')[0].get('src')
		formatted_date = format_identifier_date(details['date'])
		identifier = f"{formatted_date}|{image_link}"

		# break iteration once any registered item is matched
		if identifier in var_global.MH_NEWS_LIST:
			break

		# register new item to list
		if first_run:
			var_global.MH_NEWS_LIST.append(identifier)
			continue
		else:
			var_global.MH_NEWS_LIST.insert(0, identifier)

		details = {
			'title_link': JAPANESE_NEWS_URL,
			'image_link': image_link
		}

		# set title and color code
		category_class = article.find_class('category')[0].get('class').replace('category', '').strip()
		category, details['color_code'] = NEWS_MAPPING[category_class]
		details['title'] = f"News ({category})"

		# set description
		caption_jap = article.find_class('text')[0].text_content().strip()
		caption = (await translator.translate(caption_jap, src='ja', dest='en')).text
		article_link = article.get('href')
		details['description'] = f"[{caption}]({article_link})"

		details_list.append(details)

	# iterate through new articles, in correct order
	for details in details_list[::-1]:
		await send_news_embed(details, var_global.NEWS_CHANNEL)
