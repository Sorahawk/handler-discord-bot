from lib_imports import *


def make_get_request(url):
    proxies = {
        'http': PROXY_URL,
        'https': PROXY_URL
    }

    return requests.get(url, headers=STANDARD_HEADERS, proxies=proxies)
