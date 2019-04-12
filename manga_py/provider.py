from abc import ABCMeta

from .libs.base import Base
from .libs.meta import Chapter, File
from .libs.db import Manga, make_db
from .libs.fs import get_temp_path
from .libs.http.multi_threads import MultiThreads
from .libs.modules import verify


class Provider(Base, metaclass=ABCMeta):
    _db = None
    _store = None
    _threads = None
    _progress = None
    _api = None
    _break = False
    _allow_db = True
    _db_path = None
    temp_path_location = None
    chapter_idx = None

    def __init__(self):
        super().__init__()
        self.temp_path_location = get_temp_path()
        self._store = {}
        self._db = Manga()
        self._threads = MultiThreads()

    def run(self, args: dict):
        verify.check_url(args)
        self._args = args

        if not self.arg('no-progress'):
            self._progress = self.progressbar()
        if self.arg('no-multi-threads'):
            self._threads.max_threads = 1

        self._allow_db = not self.arg('do-not-use-database', False)

        try:
            self.loop_chapters()
        except KeyboardInterrupt:
            self.print_error('Break. Please, wait')
            self._break = True
            self.info.set_error('Break')

    def loop_chapters(self):
        if len(self.chapters):
            if isinstance(self.chapters[0][1], dict):
                self._archive_chapters()
            else:
                self._simple_chapters()

    def _archive_chapters(self):
        for idx, data in enumerate(self.chapters):
            if self._break:
                break
            chapter = Chapter(self, idx, data)
            self.before_chapter(chapter)
            self.download(chapter)
            self.after_chapter(chapter)
        self._threads.start(self.progress_next)

    def _simple_chapters(self):
        for idx, data in enumerate(self.chapters):
            if self._break:
                break
            self.chapter_idx = idx
            self.chapter = Chapter(self, idx, data)
            self.progress_next(True)
            self.before_chapter(self.chapter)
            self.loop_files()
            self.after_chapter(self.chapter)

    def loop_files(self):
        files_errors = []
        for idx, data in enumerate(self.files):
            try:
                file = File(self, idx, data)
                self._threads.add(target=self.download, args=(file,))
            except ValueError as e:
                files_errors.append((str(e), idx))
        if len(files_errors):
            self.log_warning('Files error:\n', *files_errors)
        self._threads.start(self.progress_next)

    def progress_next(self, new=False):
        """
        :param new:
        :return:
        """
        if self._progress:
            if new:
                if self._progress.value > 0:
                    self._progress.finish()
                self._progress.start(len(self._threads.threads))
            else:
                self._progress.update(self._progress.value + 1)

    def update_db(self):
        """
        Called twice.
        After receiving the content of the main page and after the completion of work.
        Updates the current manga data in the database.
        :return:
        """
        if not self._allow_db:
            return
        make_db()
        db = self._db.select().where(Manga.key == self._db_key())  # type: Manga
        if not db:
            db = Manga()
            db.key = self._db_key()
            db.name = self.manga_name
        db.url = self.main_page_url
        db.path = self.password
