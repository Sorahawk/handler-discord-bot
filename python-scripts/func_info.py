from imports import *


# checks for the latest info on Wilds
async def check_wilds_info():
	try:
		# retrieve webpage contents
		main_webpage = make_get_request(WILDS_MAIN_URL, use_proxy=True).text

		# process HTML data
		main_page_html = html.fromstring(main_webpage)
		await process_wilds_news(main_page_html)
		await process_wilds_notice(main_page_html)

	except Exception as e:
		await var_global.INFO_CHANNEL.send(f"ERROR in `check_wilds_info`: {e}")
		await var_global.INFO_CHANNEL.send(f"```{main_webpage}```")


# processes 'News' section of Wilds main page
async def process_wilds_news(html_data):
	try:
		# check for Wilds news
		news_list = html_data.find_class('news-container')[0].find_class('news-item')
		item_list = []

		for item in news_list:
			image_link = urljoin(WILDS_MAIN_URL, item.xpath('div/p/img')[0].get('src'))

			# set latest news image on first iteration
			if not var_global.LATEST_WILDS_IMAGE:
				var_global.LATEST_WILDS_IMAGE = image_link
				break

			# break iteration once latest news image is matched
			elif image_link == var_global.LATEST_WILDS_IMAGE:
				break

			details = {
				'title_link': WILDS_MAIN_URL,
				'image_link': image_link
			}

			# set title and color code
			details['title'], details['color_code'] = INFO_MAPPING['news']

			# set description
			caption = ' '.join(item.find_class('news-item__text')[0].text_content().split())
			article_link = urljoin(WILDS_MAIN_URL, item.get('href'))
			details['description'] = f"[{caption}]({article_link})"

			# format date
			date = item.find_class('news-item__ymd')[0].text_content().strip()
			input_format = '%Y.%m.%d'
			output_format = f'%A, %{UNPADDED_SYMBOL}d %B %Y'
			details['date'] = datetime.strptime(date, input_format).strftime(output_format)

			item_list.append(details)

		# iterate through new items, in correct order
		for details in item_list[::-1]:
			embed_msg, image_file = create_news_embed(details)
			await var_global.INFO_CHANNEL.send(embed=embed_msg, file=image_file)

			# update tracking of latest article sent
			var_global.LATEST_WILDS_IMAGE = details['image_link']

	except Exception as e:
		await var_global.INFO_CHANNEL.send(f"ERROR in `process_wilds_news`: {e}")


# processes 'Important Notice' section of Wilds main page
async def process_wilds_notice(html_data):
	try:

		# obtain notice list, but account for the possibility that they might remove the list entirely
		notice_list = html_data.find_class('ImportantNotice_list')

		# skip if 'Important Notice' section is missing
		if not notice_list:
			await var_global.INFO_CHANNEL.send('Important Notice section is not present on Wilds webpage.')
			return

	except Exception as e:
		await var_global.INFO_CHANNEL.send(f"ERROR in `process_wilds_notice`: {e}")
