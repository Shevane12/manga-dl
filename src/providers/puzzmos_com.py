from src.provider import Provider
from .helpers.std import Std


class PuzzmosCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        idx = self.re.search('/manga/[^/]+/([^/]+)', chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        return self._chapters('#bolumler td:first-child a')

    def get_files(self):
        img_selector = '.chapter-content img.chapter-img'
        url = self.get_current_chapter()
        parser = self.html_fromstring(url)
        pages = parser.cssselect('.col-md-12 > .text-center > select option + option')
        images = self._images_helper(parser, img_selector)
        for i in pages:
            parser = self.html_fromstring(i.get('value'))
            images += self._images_helper(parser, img_selector)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('img.thumbnail.manga-cover')


main = PuzzmosCom
