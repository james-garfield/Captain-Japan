from abc import abstractmethod
from re import split
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from src.spiders import website
from src.spiders.tag import Tag
from src.spiders.website import Website, ScrapeType
from bs4 import BeautifulSoup
import time


class Base:
    """
    Abstract class for specific methods with the scrapers.
    """
    @abstractmethod
    def load_chapters(self, chapters=None):
        """
        Get the chapters.
        """
        pass

    @abstractmethod
    def search_title(self, title, source):
        """
        Search for the title based on the source.
        """
        pass

    @abstractmethod
    def scrape(self, page):
        """
        Scrape the page
        """
        pass

    @abstractmethod
    def build_url(self, chapter):
        """
        Build the url to scrape
        """
        pass


class BaseScraper(Base):
    """
    The base for all scrapers.

    Attributes:
        - browser: selenium.webdriver.chrome.webdriver.WebDriver
            The browser that is being used to read the data.
        - website: Website
            The website that is being scraped.
    
    Properties:
        - current_url: str
            The current url of the browser.
        - page_content: str
            The content of the current page.

    Methods:
        - get(tag: Tag) -> str or List[str]
            Get the data from the tag.
        - get_attribute(tag: Tag, attribute: str, index: int = 0) -> str
            Get the attribute from the tag.
        - change_page(url: str)
            Change the page.
        - get_elements(tag: Tag) -> List[WebElement]
            Grab the elements based on the tag.

    """

    def __init__(self, website: Website, debug: bool = False) -> None:
        self.website = website
        self.browser = self.__setup__(debug)
        
    def __del__(self):
        """
        Close the browser.
        """
        self.browser.close()

    @property
    def current_url(self):
        """
        Return the browsers current url.

        :return: str
        """
        return self.browser.current_url

    @property
    def page_content(self):
        """
        Return the content of the current page.

        :return: str
        """
        return self.browser.page_source

    @property
    def soup_object(self):
        """
        Return the content of the current page as a soup object.
        
        Returns: BeautifulSoup
        """
        return BeautifulSoup(self.page_content, "html.parser")

    def __setup__(self, debug: bool):
        """
        Setup the browser.

        Params:
            - debug: bool
                Whether to show the browser in debug mode.
        
        Returns: <Selenium>
        """
        options = Options()
        # Check if debug mode is enabled.
        options.headless = not debug

        # Options to act as a real user. To bypass the captcha and cloudflare.
        options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        options.add_argument("--lang=en-US")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # Bypass cloudflare detection.
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Return the browser.
        return browser

    def change_page(self, url: str, sleep=True):
        """
        Change the page.

        Params:
            - url: str
                The url to change to.
            - sleep: bool
                Whether to sleep after changing the page.
        """
        self.browser.get(url)
        if sleep:
            time.sleep(2)

    def get(self, tag: Tag):
        """
        Get the data from the tag.

        Params:
            - tag: Tag
                The tag to get the data from.
        
        Returns: str or list[str]
        """
        # Get the elements.
        elements = self.browser.find_elements(tag.tag_type, tag.tag_value)

        # Check if elements has more than one element.
        if len(elements) > 1:
            # Return the list of elements.
            return [e.text for e in elements]

        # Return the text of the element.
        return elements[0].text

    def get_attribute(self, tag: Tag, attribute: str, index: int = 0):
        """
        Get the attribute from the tag.

        Params:
            - tag: Tag
                The tag to get the data from.
            - attribute: str
                The attribute to get.
            - index: int
                The index of the element to get the attribute from.

        Returns: str
        """
        # Get the elements.
        elements = self.browser.find_elements(tag.tag_type, tag.tag_value)

        # Return the attribute.
        return elements[index].get_attribute(attribute)

    def get_elements(self, tag):
        """
        Grab the elements based on the tag.

        Params:
            - tag: Tag
                The tag to get the data from.
        
        Returns: list[WebElement]
        """
        # Get the elements.
        elements = self.browser.find_elements(tag.tag_type, tag.tag_value)

        # Return the elements.
        return elements

    def get_cover_image(self):
        """
        Get the cover image of the title.

        Returns: str
        """
        # Get the cover image.
        cover_image = self.get_attribute(self.website.cover_image_tag, "src", 0)

        # Return the cover image.
        return cover_image

    def get_title(self):
        """
        Get the title of the manga or novel.
        """
        soup = self.soup_object
        try:
            # Get the title.
            title = soup.find(self.website.title_tag.tag, {self.website.title_tag.tag_type_soup: self.website.title_tag.tag_value}).text
            # Return the title.
            return title
        except AttributeError:
            # Return None.
            return None

    def get_description(self):
        """
        Get the description of the manga or novel.
        """
        soup = self.soup_object
        try:
            # Get the description.
            description = soup.find(self.website.description_tag.tag, {self.website.description_tag.tag_type_soup: self.website.description_tag.tag_value}).text
            # Return the description.
            return description
        except AttributeError:
            # Return None.
            return None

    def get_main_body(self):
        """
        Get the main body of the page where the magic happens! (Where the data we scrape is)
        """
        soup = self.soup_object
        try:
            # Get the main body.
            main_body = soup.find(self.website.main_body_tag.tag, {self.website.main_body_tag.tag_type_soup: self.website.main_body_tag.tag_value}).text
            # Return the main body.
            return main_body
        except AttributeError:
            # Return None.
            return None

    def get_chapter_links(self):
        """
        Get the chapter links.

        Returns: list[str] | list[WebElement]
        """
        # This method does not know how to get the link of the source.
        if self.website.base_url not in self.current_url:
            raise(
                Exception("The current url is not from the base.")
            )

        # Check if the Wesbite has a chapters_args
        if self.website.chapters_args is None:
            # We just need to do a soup object
            soup = self.soup_object
            # Get the chapter links.
            chapter_links = soup.find(self.website.chapters_tag.tag, {self.website.chapters_tag.tag_type_soup: self.website.chapters_tag.tag_value})
            # Return the chapter links.
            return [c["href"] for c in chapter_links.find_all("a")]
        else:
            # We need to use Selenium
            self.change_page(self.website.chapter_url(self.current_url))
            # Get the chapter links.
            chapter_links = self.get_elements(self.website.chapters_tag)
            # Parsing must be done on reciever
            return chapter_links