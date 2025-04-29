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
		article_list = []
		translator = googletrans.Translator()

		for article in news_list:
			image_link = article.xpath('li/figure/img')[0].get('src')

			# set latest article image on first iteration
			if not var_global.LATEST_NEWS_IMAGE:
				var_global.LATEST_NEWS_IMAGE = image_link
				return

			# break iteration once latest article image is matched
			elif image_link == var_global.LATEST_NEWS_IMAGE:
				break

			details = {
				'image_link': image_link,
				'article_link': article.get('href')
			}

			# format date
			date = article.find_class('date')[0].text_content().strip()
			input_format = '%Y.%m.%d'
			output_format = f'%A, %{UNPADDED_SYMBOL}d %B %Y'
			details['date'] = datetime.strptime(date, input_format).strftime(output_format)

			# extract specific category
			category_class = article.find_class('category')[0].get('class').replace('category', '').strip()
			details['category'], details['color_code'] = NEWS_MAPPING[category_class]

			# translate Japanese text to English
			details['caption_jap'] = (caption_jap := article.find_class('text')[0].text_content().strip())
			details['caption_eng'] = (await translator.translate(caption_jap, src='ja', dest='en')).text

			article_list.append(details)

		# iterate through new articles, in correct order
		for details in article_list[::-1]:
			embed_msg, image_file = create_news_embed(details)
			await var_global.NEWS_CHANNEL.send(embed=embed_msg, file=image_file)

			# update tracking of latest article sent
			var_global.LATEST_NEWS_IMAGE = details['image_link']

	except Exception as e:
		await var_global.NEWS_CHANNEL.send(f"ERROR in `check_latest_news`: {e}")
		await var_global.NEWS_CHANNEL.send(f"```{news_webpage}```")
