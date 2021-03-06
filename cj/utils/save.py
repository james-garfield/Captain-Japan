# Handles the saving of the files.
from cj.objects.chapter import Chapter
from cj.objects.source import Source
from cj.utils.enums import CjType
from cj.utils.naming import remove_chars
from cj.utils.path import create_dir, create_source_path
from cj.data.cj_db import CJDB
from threading import Thread

import codecs
import os
import shutil


class Save:
    """
    Handles the writing to files and Database when adding Novels, Mangas, or Anime.
    """
    def __init__(self, chapter: Chapter, source: Source) -> None:
        self.chapter = chapter
        self.source = source
        self.db = CJDB()

        Thread(target=self.save).start()

    def save(self) -> None:
        """
        Save the chapter body to the source.
        """
        # Raise error if chapter.number is not set
        if self.chapter.number is None:
            raise ValueError("Chapter number is not set")
        # Raise error if chapter.body is not set
        if self.chapter.body is None:
            raise ValueError("Chapter body is not set")

        # First check if the source has a location
        if self.source.location is None:
            # Go ahead and create the dir
            location = create_source_path(self.source, self.source.directory())
            self.source.location = location
            # Save the source
            self._save_to_db()

        # Ok the location is set, now save the chapter
        self._save_chapter()

    def _save_to_db(self):
        """
        Save to the database the current source of the Save class.
        """
        if self.source.cj_type is CjType.NOVEL:
            self.db.add_novel(self.source)
        # elif self.source.cj_type is CjType.MANGA:
        #     self.db.add_manga(self.source)

    def _save_chapter(self):
        """
        Actually Save the chapter
        """
        # Check first if the chapter exists
        chapter_path = self.source.chapter_path(self.chapter.number)
        if os.path.exists(chapter_path):
            # Remove that fucker
            try:
                os.rmdir(chapter_path)
            except OSError:
                shutil.rmtree(chapter_path)
        # Create the chapter dog
        create_dir(chapter_path)

        # Writing the TXT
        with codecs.open(f"{chapter_path}/{remove_chars(self.chapter.title)}.txt", "w", "utf8") as file:
            file.write(self.chapter.body)
        
        # Writing the HTML
        with codecs.open(f"{chapter_path}/{remove_chars(self.chapter.title)}.html", "w", "utf8") as file:
            file.write(self.chapter.document)