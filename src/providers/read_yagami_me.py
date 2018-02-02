from src.provider import Provider


class ReadYagamiMe(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return '{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re_search('/read/[^/]+/(\\d+)/(.+)/', self.get_current_chapter()).groups()
        return '{}-{}'.format(*idx).replace('/', '.')

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/series/{}/'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re_search('/(?:series|read)/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        items = self.document_fromstring(self.get_storage_content(), '#midside .group .element .title a')
        return [i.get('href') for i in items]

    def prepare_cookies(self):
        pass

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), '.web_pictures img.web_img')
        return [i.get('src') for i in items]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = ReadYagamiMe