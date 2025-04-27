from imports import *


# monitors 'News' and 'Important Notice' sections of Wilds main page
def check_wilds_main():
	# retrieve webpage contents
#	main_webpage = make_get_request(WILDS_MAIN_URL, use_proxy=True).text
	main_webpage = make_get_request(WILDS_MAIN_URL).text

	# process HTML data
	html_data = html.fromstring(main_webpage)
	news_list = html_data.find_class('news-container')[0]
	notice_list = html_data.find_class('ImportantNotice_list')[0]

	



# checks for the latest info on Wilds
async def check_wilds_info():
	try:
		pass

	except Exception as e:
		await channel.send(f"ERROR in `check_wilds_info`: {e}")
		await channel.send(f"```{main_webpage}```")



if __name__ == '__main__':
	check_wilds_main()
