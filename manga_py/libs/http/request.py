from random import randint

import requests
from copy import copy


class Request(object):
    _req = None
    _headers = None
    _cookies = None

    def __init__(self):
        self._req = requests
        self._headers = {}
        self._cookies = {}

    @property
    def ua(self):
        ua = self._headers.get('User-Agent', None)
        if ua is None:
            ua = self._user_agent()
            self._headers['User-Agent'] = ua
        return ua

    @ua.setter
    def ua(self, ua):
        self._headers['User-Agent'] = ua

    def set_lang(self, lang='en-US'):
        self._headers['Accept-Language'] = '%s;q=0.9,ja-JP;q=0.8' % lang

    def set_referer(self, referer):
        self._headers['referer'] = referer

    def check_url(self, url):
        return self.request('head', url).ok

    def get(self, url, *args, **kwargs) -> requests.Response:
        return self.request('get', url, *args, **kwargs)

    def post(self, url, *args, **kwargs) -> requests.Response:
        return self.request('post', url, *args, **kwargs)

    def request(self, method, url, *args, **kwargs) -> requests.Response:
        request = getattr(requests, method)  # get/post/head/ etc
        kwargs.setdefault('headers', self._headers)
        kwargs.setdefault('cookies', self._cookies)
        return request(url, *args, **kwargs)

    @classmethod
    def _user_agent(cls, agent=None) -> str:
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
            'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
        ]
        if agent is None:
            agent = agents[randint(0, len(agents) - 1)]
        return agent

    def _update_cookies(self, response: requests.Response):
        for element in response.history:  # type: requests.Response
            self._cookies.update(element.cookies.get_dict())
        self._cookies.update(response.cookies.get_dict())

    def copy(self):
        return copy(self)
