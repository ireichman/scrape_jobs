"""

"""
from bs4 import BeautifulSoup as bs
import requests
from loguru import logger
import re

class HTML:

    def __init__(self, html_raw: object, keywords: list = None, website: str = None):
        self.soup = bs(markup=html_raw.content, features="html.parser")
        self.html_body = self.soup.find("body")
        self.prettify = self.html_body.prettify()
        self.keywords: list = keywords
        self.element: object = None
        self.elements: list = []
        self.elements_with_keywords: list = []
        logger.info(f"Created HTML object for {website} with keywords: {keywords}")

    def search_for_elements(self, element_type: str, text_content: str):
        """
        Find HTML elements whose string match any of the strings in string_text. Optionally, Specify a different HTML
        attribute that string_text should match.
        :param element_type: Specify what type of element to search for.
        :param string_text: A list of strings to search for in the html 'string' attribute (unless element_attribute is
        specified).
        :param element_attribute: Optionally, specify an HTML attribute to search in instead of 'string'.
        :return: ???
        """
        #
        logger.info(f"Searching for HTML tag '{element_type}' with attribute: text_content={text_content}, "
                    f"containing string(s):")
        # word = lambda text: **[attribute_value[0]] in text.lower()
        # try:
        #     all_found_elements = self.html_body.find_all(name=element_type, href=True)
        #
        #     all_elements_with_career = []
        #     for element in all_found_elements:
        #         if re.search(pattern="career", string=element.text.lower()):
        #             all_elements_with_career.append(element)
        #             logger.info(f"FOUND ELEMENT: {element}")
        #             self.element = element
        #             return self.element
        #     # logger.info(f"Search for HTML elements found: {element}")
        #     # return all_elements_with_career
        # except AttributeError as error:
        #     logger.error(f"Searching for HTML element returned error: {error}")

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
            for keyword in keywords:
                logger.info(f"Searching for '{keyword}' in {str(element)}")
                if re.search(pattern=keyword, string=str(element).lower()):
                    logger.info(f"FOUND {keyword} in {str(element).lower()}")
                    if element not in self.elements_with_keywords:
                        self.elements_with_keywords.append(element)
                        logger.info(f"Added {element}\n to self.elements_with_keyword based on keyword: {keyword}")
        return self.elements_with_keywords

