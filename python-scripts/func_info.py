from imports import *


# checks for the latest info on Wilds
async def check_wilds_info():
	try:
		# retrieve webpage contents
		main_webpage = make_get_request(WILDS_MAIN_URL, use_proxy=True).text

		# process HTML data
		html_data = html.fromstring(main_webpage)

		# obtain news list
		news_list = html_data.find_class('news-container')[0]

		# obtain notice list, but account for the possibility that they might remove the list entirely
		notice_list = html_data.find_class('ImportantNotice_list')


	except Exception as e:
		await var_global.INFO_CHANNEL.send(f"ERROR in `check_wilds_info`: {e}")
		await var_global.INFO_CHANNEL.send(f"```{main_webpage}```")


# processes 'News' and 'Important Notice' sections of Wilds main page
def process_wilds_main(news_list, notice_list):



	# skip if 'Important Notice' section is missing
	if not notice_list:
		# TODO: display warning?
		# worth a look if it actually happens
		return
