from imports import *


# Discord is unable to get image content on its own, possibly due to headers being rejected by MH website
# Thus, obtain image data to pass into Discord directly
async def add_embed_image(image_link, embed_msg, use_proxy=False):
	image_data = await make_get_request(image_link, use_proxy, get_content=True)
	image_file = discord.File(io.BytesIO(image_data), filename="image.jpg")

	embed_msg.set_image(url="attachment://image.jpg")
	return embed_msg, image_file


# returns a formatted embed message containing quest details
async def send_quest_embed(quest_details, channel):
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

	embed_msg, image_file = await add_embed_image(quest_details['image_link'], embed_msg)
	await channel.send(embed=embed_msg, file=image_file)


# returns a formatted embed message containing news and info details
async def send_news_embed(details, channel):
	embed_msg = discord.Embed(title=details['title'], url=details['title_link'], description=details['description'], color=details['color_code'])

	output_format = f'%A, %{UNPADDED_SYMBOL}d %B %Y'
	embed_msg.set_footer(text=details['date'].strftime(output_format))

	# additional fields for Update
	if 'release_date' in details:
		embed_msg.add_field(name=details.get('contents_header', 'Details'), value=details['contents'], inline=False)
		embed_msg.add_field(name='Release Date', value=details['release_date'].strftime(output_format), inline=False)
		embed_msg.add_field(name='Platforms', value=details['platforms'], inline=False)

	# additional fields for Support
	elif 'issue_cat' in details:
		embed_msg.add_field(name='Categories', value=details['issue_cat'], inline=False)
		embed_msg.add_field(name='Platforms', value=details['platforms'], inline=False)

	if 'image_link' in details:
		embed_msg, image_file = await add_embed_image(details['image_link'], embed_msg, use_proxy=True)
		await channel.send(embed=embed_msg, file=image_file)
	else:
		await channel.send(embed=embed_msg)
