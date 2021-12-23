from selenium.webdriver.common.by import By
from cj.scraper.base import NoSoupException, Scraper
from abc import abstractmethod

from cj.utils.chapter import Chapter


class NovelBase(Scraper):
    """
    This is mostly a abstract class.
    
    Methods:
        - build_url(chapter): The chapter number to load for the URL.
        - load_chapters(url): The url that holds all the chapters is passed and uses it to scrape.
        - scrape(chapter): Scrape the body from the page of the chapter number passed.
    
    Params:
        - headless(bool): Is this a headless browser? Defaults to true.
        - javascript(bool): Does the website need Javascript to render?
        - url(str): The url of the Novel website.
        - title(str): The title of the novel to scrape.
    """
    def __init__(self, javascript: bool, headless: bool, url: str, title: str,) -> None:
        super().__init__(javascript, headless, start_url=url)
        self.base_url = url
        self.title = title
        self.chapters: list[Chapter] = []

    @abstractmethod
    def build_url(self, chapter: int) -> str:
        """
        Get the url for a chapter

        Params:
            - chapter(int): The chapter number (or index in list) to build the url for.

        Returns:
            - The url for the chapter.
        """
        raise NotImplementedError
    
    @abstractmethod
    def load_chapters(self, url: str) -> None:
        """
        Load all the chapters for this novel.

        Params:
            - url(str): The url to load the chapters from.
        """
        raise NotImplementedError

    @abstractmethod
    def scrape(self, chapter: int) -> None:
        """
        Scrape the novel body for the chapter passed.

        Params:
            - chapter(int): The chapter number to scrape.
        """
        raise NotImplementedError

    @staticmethod
    def search(self) -> str:
        """
        Search the novel for the title passed.

        Returns:
            - The url of the novel.
        """
        raise NotImplementedError

    @staticmethod
    def cover(self) -> str:
        """
        Get the cover image of the novel.

        Returns:
            - The url of the cover image.
        """
        raise NotImplementedError

    def get_chapter(self, url):
        """
        Get the page contents of the url passed.

        Params:
            - url(str): The url to get.
            - scroll_distance(int): The distance to scroll the page.

        Returns:
            - The page contents.
        """
        previous_url = self.current_url
        # Set the current url
        self.current_url = url
        soup_object = self.soup(5)

        # Raise a exception if the soup object is not found.
        if soup_object is None:
            # Reset the current url
            self.current_url = previous_url
            raise NoSoupException

        # Otherwise, return the soup object.
        return soup_object