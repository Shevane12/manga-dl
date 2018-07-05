from lxml.html import document_fromstring, Element
from manga_py.libs.http import Http
from tinycss import make_parser


class Html:
    http = None

    def __init__(self, http: Http):
        self.http = http

    def from_content(self, content, selector: str = None, idx: int = None):
        html = document_fromstring(content)
        if selector is not None:
            html = html.cssselect(selector)
            if idx is not None and len(html) > idx:
                return html[idx]
        return html

    def from_url(self, url, selector: str = None, idx: int = None):
        content = self.http.get(url).text
        return self.from_content(content, selector, idx)

    def _check_parser(self, parser):
        if isinstance(parser, str):
            parser = self.from_content(parser)
        elif not isinstance(parser, Element):
            raise AttributeError('Undefined type')
        return parser

    def elements(self, parser, selector: str):
        """
        :param parser: str|Element
        :param selector: str
        :return:
        """
        return self._check_parser(parser).cssselect(selector)

    def _cover_from_tuple(self, item: Element, attributes):
        for attr in attributes:
            value = item.get(attr, None)
            if value is None:
                continue
            value = self.http.normalize_uri(value)
            test = self.http.check_url(value)
            if test:
                return value
        return None

    @staticmethod
    def _cssselect(parser: Element, selector) -> list:
        if selector is None:
            return [parser]
        return parser.cssselect(selector)

    def cover(self, parser, selector: str, attribute='src', index: int = 0):
        """
        :param parser: str|Element
        :param selector: str
        :param attribute: str|tuple
        :param index: int
        :return:
        """
        parser = self._check_parser(parser)
        items = self._cssselect(parser, selector)
        if len(items) > index:
            if isinstance(attribute, str):
                return items[index].get(attribute, None)
            if isinstance(attribute, tuple):
                return self._cover_from_tuple(items[index], attribute)
        return None

    def parse_background(self, element: Element) -> str:
        """
        :param element:
        :return:
        """
        style = element.get('style', None)
        value = None
        if style:
            css = make_parser(style)
            try:
                value = css.parse_style_attr(style)[0][0].value[0].value
            except IndexError:
                pass
        return self.http.normalize_uri(value)

    def text_content(self, parser, selector: str, idx: int = 0, strip: bool = True):
        items = self._cssselect(parser, selector)
        text = items[idx].text_content()
        if strip:
            text = text.strip()
        return text
