"""
Scraping tools and classes
"""
from bs4 import BeautifulSoup as bs
from loguru import logger
import re


class HTML:
    """
    HTML handling using BS4.
    """
    def __init__(self, html_raw: object, website: str, keywords: list = None):
        """
        HTML class is initialized with a requests object of the jobs page from a site.
        :param html_raw: requests object
        :param website: A string with the URL of the HTML page.
        :param keywords: list of strings. Each string can be used for searching in job descriptions.
        """
        self.soup = bs(markup=html_raw, features="html.parser")
        self.html_body = self.soup.find("body")
        # Prettify shows HTML in a pretty format for debugging purposes.
        self.prettify = self.html_body.prettify()
        # Using set for faster match search.
        self.href_keywords: set = {"career", "careers", "job", "jobs"}
        self.keywords: list = keywords
        self.element: object = None
        self.elements: list = []
        self.elements_with_keywords: list = []
        self.website: str = website
        logger.info(f"Created HTML object for {self.website} with keywords: {keywords}")

    def search_for_elements(self, element_type: str, text_content: str):
        """
        Searches BS4 soup for elements of a specific type with a specific text content.
        :param element_type: Specify the HTML element to look for.
        :param text_content: Specify the text in the HTML element.
        :return: A BS4 object.
        """
        logger.info(f"Searching for HTML tag '{element_type}' with attribute: text_content={text_content}, "
                    f"containing string(s):")

        try:
            all_elements = self.html_body.find_all(name=element_type, href=self.search_in_href)
            logger.info(f"Found elements: {all_elements}")
            self.elements = all_elements
            logger.debug(f"Self.elements = {self.elements}")
            return all_elements
        except Exception as error:
            logger.error(f"Searching for element(s) error: {error}")

    def extract_from_element(self, what_to_extract: str):
        """

        :param what_to_extract:
        :return:
        """
        logger.info(f"Extracting from element: {what_to_extract}")
        try:
            extracted_data = self.element[what_to_extract]
            logger.info(f"Extracted data: {extracted_data}")
            return extracted_data
        except Exception as error:
            logger.error(error)

    def keywords_search(self, keywords: list):
        """
        Take a list of BS objects and search for keywords in them. Add those elements to self.element_with_keywords
        :param keywords: list of keywords passed by the user.
        :return: A list of BS4 objects that matches any of the keywords.
        """

        for element in self.elements:
            element_string = str(element).lower()
            for keyword in keywords:
                logger.info(f"Searching for '{keyword}' in {element_string}")
                if re.search(pattern=f'(?<!\\w){keyword}(?!\\w)', string=element_string):
                    logger.info(f"FOUND {keyword} in {element_string}")
                    if element not in self.elements_with_keywords:
                        self.elements_with_keywords.append(element)
                        logger.info(f"Added {element}\n to self.elements_with_keyword based on keyword: {keyword}")
        logger.info(f"Found {len(self.elements_with_keywords)} elements with keywords")
        return self.elements_with_keywords

    def search_in_element(self, element: str):
        element_to_set = set(element.split())
        # Keywords to search for in href.
        href_key_words = ["career", "job", "opportunity"]

    def search_in_href(self, href: str):
        if href:
            words = re.split(r'\W+', href)
            return any(word in words for word in self.href_keywords)
        return False
