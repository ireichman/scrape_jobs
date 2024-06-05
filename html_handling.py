"""
Scraping tools and classes
"""
from bs4 import BeautifulSoup as bs
import requests
from loguru import logger
import re


class HTML:
    """
    HTML handling using BS4.
    """
    def __init__(self, html_raw: object, keywords: list = None):
        """
        HTML class is initialized with a requests object of the jobs page from a site.
        :param html_raw: requests object
        :param keywords: list of strings. Each string can be used for searching in job descriptions.
        """
        self.soup = bs(markup=html_raw.content, features="html.parser")
        self.html_body = self.soup.find("body")
        # Prettify shows HTML in a pretty format for debugging purposes.
        self.prettify = self.html_body.prettify()
        self.keywords: list = keywords
        self.element: object = None
        self.elements: list = []
        self.elements_with_keywords: list = []
        logger.info(f"Created HTML object for {html_raw.url} with keywords: {keywords}")

    def search_for_elements(self, element_type: str, text_content: str):
        """

        :param element_type:
        :param text_content:
        :return:
        """
        logger.info(f"Searching for HTML tag '{element_type}' with attribute: text_content={text_content}, "
                    f"containing string(s):")

        try:
            all_elements = self.html_body.find_all(name=element_type, href=True)
            logger.info(f"Found elements: {all_elements}")
            self.elements = all_elements
            logger.debug(f"Self.elements = {self.elements}")
            return all_elements
        except Exception as error:
            logger.error(f"Searching for element(s) error: {error}")

    def extract_from_element(self, what_to_extract: str):
        """
        Finds data in BS object.
        :param element_object:
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
        :return: self.element_with_keywords
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

