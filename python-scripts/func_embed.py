from func_http import *


# Discord is unable to get image content on its own, possibly due to headers being rejected by MH website
# Thus, obtain image data to pass into Discord directly
def add_embed_image(image_url, embed_msg, use_proxy=False):
	image_data = make_get_request(image_url, use_proxy).content
	image_file = discord.File(io.BytesIO(image_data), filename="image.jpg")

	embed_msg.set_image(url="attachment://image.jpg")
	return embed_msg, image_file


# returns a formatted embed message containing news details
def create_news_embed(news_details):
	embed_msg = discord.Embed(title=news_details['caption_eng'], url=news_details['article_link'], timestamp=news_details['timestamp'], color=news_details['color_code'])
	embed_msg.set_footer(text=news_details['category'])

	embed_msg, image_file = add_embed_image(news_details['image_link'], embed_msg, use_proxy=True)
	return embed_msg, image_file


# returns a formatted embed message containing quest details
def create_quest_embed(quest_details):
	embed_msg = discord.Embed(title=quest_details['title'], url=EVENT_QUEST_URL, color=quest_details['color_code'])
	embed_msg.add_field(name='Description', value=quest_details['description'], inline=False)

	embed_msg.add_field(name='Objective', value=quest_details['completion_conditions'], inline=True)
	embed_msg.add_field(name='Locale', value=quest_details['locales'], inline=True)
	embed_msg.add_field(name='Difficulty', value=quest_details['difficulty'], inline=True)

	# format dates
	input_format = '%m.%d.%Y %H:%M'
	output_format = f'%a, %{UNPADDED_SYMBOL}d %b, %{UNPADDED_SYMBOL}I:%M %p'
	start_date = datetime.strptime(quest_details['start_date_and_time'], input_format).strftime(output_format)
	end_date = datetime.strptime(quest_details['end_date_and_time'], input_format).strftime(output_format)

	embed_msg.add_field(name='Category', value=quest_details['category_name'], inline=True)
	embed_msg.add_field(name='Start', value=start_date, inline=True)
	embed_msg.add_field(name='End', value=end_date, inline=True)

	embed_msg, image_file = add_embed_image(quest_details['image_url'], embed_msg)
	return embed_msg, image_file
