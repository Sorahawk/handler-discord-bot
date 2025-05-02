from imports import *


# obtains full traceback of given exception and outputs to specified channel
async def send_traceback(e, channel):
	full_trace = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
	await channel.send(f'```{full_trace}```')
