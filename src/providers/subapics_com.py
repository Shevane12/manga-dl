from src.providers.mangashiro_net import MangaShiroNet
from .helpers.std import Std


class SubaPicsCom(MangaShiroNet, Std):
    alter_re_name = r'\.(?:com|net)/([^/]+)\-chapter-\d+'
    chapter_re = r'\-chapter\-(\d+(?:\-\d+)?)'

    def get_cover(self) -> str:
        return self._cover_from_content('.imgdesc > img')

    def get_files(self):
        url = self.get_current_chapter()
        parser = self.html_fromstring(url)
        items = parser.cssselect('#readerarea img')
        return [i.get('src') for i in items]


main = SubaPicsCom
