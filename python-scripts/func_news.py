from imports import *


# checks for the latest news articles
async def check_latest_news():
	try:
		# retrieve webpage contents via proxy because `www` subdomain seems to be stricter than `info`
		news_webpage = make_get_request(JAPANESE_NEWS_URL, use_proxy=True).text

		# process HTML data
		html_data = html.fromstring(news_webpage)
		news_list = html_data.find_class('mhNews_list')[0]

		# check for new articles
		details_list = []
		translator = googletrans.Translator()

		for article in news_list:
			image_link = article.xpath('li/figure/img')[0].get('src')

			# set latest article image on fresh startup
			if not var_global.LATEST_NEWS_IMAGE:
				var_global.LATEST_NEWS_IMAGE = image_link
				return

			# break iteration once latest article image is matched
			elif image_link == var_global.LATEST_NEWS_IMAGE:
				break

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

			# format date
			date = article.find_class('date')[0].text_content().strip()
			input_format = '%Y.%m.%d'
			details['date'] = datetime.strptime(date, input_format)

			details_list.append(details)

		# iterate through new articles, in correct order
		for details in details_list[::-1]:
			await send_news_embed(details, var_global.NEWS_CHANNEL)

			# update tracking of latest article sent
			var_global.LATEST_NEWS_IMAGE = details['image_link']

	except Exception as e:
		await send_traceback(e, var_global.NEWS_CHANNEL)
