from src.provider import Provider
from .helpers.std import Std


class MangaKakalotCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/chapter_([^/]+)', self.get_current_chapter()).split('.')
        return '{}-{}'.format(*self._idx_to_x2(idx))

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/(?:manga|chapter)/([^/]+)/?', self.get_url())

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), '.chapter-list span a')

    def get_files(self):
        result = self.html_fromstring(self.get_current_chapter(), '#vungdoc img')
        return [i.get('src') for i in result]


main = MangaKakalotCom
