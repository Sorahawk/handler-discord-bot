import io, requests

from global_constants import *

from discord import File


# Discord is unable to get image content on its own, possibly due to headers being rejected by MH website
# Thus, obtain image data to pass into Discord directly
def add_embed_image(image_url, embed_msg):
	image_data = requests.get(image_url, headers=STANDARD_HEADERS).content

	image_file = File(io.BytesIO(image_data), filename="image.jpg")
	embed_msg.set_image(url="attachment://image.jpg")

	return embed_msg, image_file
