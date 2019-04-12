from typing import List, Union

from lxml.etree import ElementBase
from lxml.html import document_fromstring
from requests import Response
from tinycss import make_parser

from manga_py.libs.http import Http


class Html:
    http = None

    def __init__(self, http: Http):
        self.http = http

    @staticmethod
    def _check_response(response) -> str:
        if isinstance(response, Response):
            response = response.content
        return response

    @staticmethod
    def from_content(content, selector: str = None, idx: int = None) -> Union[ElementBase, List[ElementBase]]:
        """
        :param content: str
        :param selector: str
        :param idx: int
        :return: Union[ElementBase, list]
        """
        content = Html._check_response(content)
        html = document_fromstring(content)
        if selector is not None:
            html = html.cssselect(selector)
            if idx is not None and len(html) > idx:
                return html[idx]
        return html

    def from_url(self, url, selector: str = None, idx: int = None) -> Union[ElementBase, List[ElementBase]]:
        """
        :param url: str
        :param selector: str
        :param idx: int
        :return: Union[ElementBase, list]
        """
        content = self.http.get(url).text
        return self.from_content(content, selector, idx)

    def _check_parser(self, parser) -> ElementBase:
        if isinstance(parser, str):
            parser = self.from_content(parser)
        elif not isinstance(parser, ElementBase):
            raise TypeError('parser type error')
        return parser

    def elements(self, parser: Union[str, ElementBase], selector: str) -> List[ElementBase]:
        """
        :param parser: str|ElementBase
        :param selector: str
        :return:
        """
        return self._check_parser(parser).cssselect(selector)

    def _cover_from_tuple(self, item: ElementBase, attributes):
        for attr in attributes:
            value = item.get(attr, None)
            if value is None:
                continue
            value = self.http.normalize_uri(value)
            test = self.http.check_url(value)
            if test:
                return value
        return None

    @classmethod
    def _cssselect(cls, parser: ElementBase, selector) -> List[ElementBase]:
        if selector is None:
            return [parser]
        return parser.cssselect(selector)

    def cover(self, parser: Union[str, ElementBase], selector: str,
              attribute: Union[str, tuple] ='src', index: int = 0) -> Union[None, str]:
        """
        :param parser: str or ElementBase
        :param selector: str
        :param attribute: str or tuple
        :param index: int
        :return:
        """
        parser = self._check_parser(parser)
        items = self._cssselect(parser, selector)  # type: List[ElementBase]
        if len(items) > index:
            if isinstance(attribute, str):
                return items[index].get(attribute, None)
            if isinstance(attribute, tuple):
                return self._cover_from_tuple(items[index], attribute)
        return None

    def parse_background(self, element: ElementBase) -> str:
        """
        :param element:
        :return:
        """
        style = element.get('style', None)
        value = None
        if style:
            css = make_parser(None)
            try:  # do not touch this!
                for declaration in css.parse_style_attr(style)[0]:
                    if declaration.name == 'background':
                        for token in declaration.value:
                            if token.type == 'URI':
                                value = token.value
                                break
                    if declaration.name == 'background-image':
                        value = declaration.value[0].value
                        break
            except IndexError:
                return ''
        return self.http.normalize_uri(value)

    def text_content(self, parser, selector: str, idx: int = 0, strip: bool = True) -> str:
        items = self._cssselect(parser, selector)
        text = items[idx].text
        return text.strip() if strip else text

    def attribute_values(self, parser, selector: str = 'img', attr='src'):
        items = self._check_parser(parser).cssselect(selector)
        return [i.get(attr) for i in items]

    def images(self, parser, selector, attr='src') -> list:
        image = self._cssselect(parser, selector)
        return [i.get(attr).strip(' \r\n\t\0') for i in image]
