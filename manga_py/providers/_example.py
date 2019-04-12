from typing import List
from requests import Response

from manga_py.libs.http import Http
from manga_py.provider import Provider


# see manga_py/libs/base/abstract.py for more data
class Example(Provider):

    def get_main_page_url(self) -> str:
        pass

    def get_content(self) -> Response:
        pass

    def get_manga_name(self) -> str:
        pass

    def get_chapters(self) -> list:
        pass

    def get_files(self) -> list:
        pass

    def get_chapter_name(self, chapter) -> str:
        pass

    def get_chapter_url(self) -> str:
        pass

    def before_provider(self, args: dict):
        pass

    def after_provider(self):
        pass

    # need overload, but not required methods:
    def get_cover(self) -> str:
        pass

    def get_meta(self):
        pass

    @staticmethod
    def search(title: str, http: Http) -> List[str]:
        pass


main = Example  # Required!
