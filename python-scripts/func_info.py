from imports import *


# checks for the latest info on Wilds
async def check_wilds_info():
	try:
		pass

	except Exception as e:
		await var_global.INFO_CHANNEL.send(f"ERROR in `check_wilds_info`: {e}")
		await var_global.INFO_CHANNEL.send(f"```{main_webpage}```")


# processes 'News' and 'Important Notice' sections of Wilds main page
def process_wilds_main():
	# retrieve webpage contents
	#main_webpage = make_get_request(WILDS_MAIN_URL, use_proxy=True).text


	with open('mainpage.html', encoding='utf-8') as infile:
		main_webpage = '\n'.join(infile.readlines())


	# process HTML data
	html_data = html.fromstring(main_webpage)

	# process news list
	news_list = html_data.find_class('news-container')[0].find_class('news-item')
	latest_image_link = urljoin(WILDS_MAIN_URL, news_list[0].xpath('div/p/img')[0].get('src'))

	# set latest news image
	if not var_global.LATEST_WILDS_IMAGE:
		var_global.LATEST_WILDS_IMAGE = latest_image_link

	# new items detected
	elif latest_image_link != var_global.LATEST_WILDS_IMAGE:
		item_list = []

		for item in news_list:
			details = {}

			# extract image




	# obtain notice list, but account for the possibility that they might remove the list entirely
	notice_list = html_data.find_class('ImportantNotice_list')

	# skip if 'Important Notice' section is missing
	if not notice_list:
		# TODO: display warning?
		# worth a look if it actually happens
		return





if __name__ == '__main__':
	process_wilds_main()
