from import_lib import *


def make_get_request(url, use_proxy=False):
	if not use_proxy:
		return requests.get(url, headers=STANDARD_HEADERS)

	else:
		proxy_protocol, proxy_domain_port = PROXY_URL.split('//')
		proxy_auth_url = f'{proxy_protocol}//{PROXY_USERNAME}:{PROXY_PASSWORD}@{proxy_domain_port}'

		proxies = {
			'http': proxy_auth_url,
			'https': proxy_auth_url
		}

		return requests.get(url, headers=STANDARD_HEADERS, proxies=proxies)
