"""

"""
from bs4 import BeautifulSoup as bs
import requests
from loguru import logger
import re

class HTML:

    def __init__(self, html_raw: object, keywords: list, website: str):
        self.soup = bs(markup=html_raw.content, features="html.parser")
        self.html_body = self.soup.find("body")
        self.prettify = self.html_body.prettify()
        self.keywords: list = keywords
        logger.info(f"Created HTML object for {website} with keywords: {keywords}")

    def search_elements(self, element_type: str, text_content: str):
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
        try:
            all_found_elements = self.html_body.find_all(name=element_type)

            all_elements_with_career = []
            for element in all_found_elements:
                if re.search("career", element.text.lower()):
                    all_elements_with_career.append(element)
                    logger.info(f"FOUND ELEMENT: {element}")
                    logger.info(f"THE HREF= {element}")



            # logger.info(f"Search for HTML elements found: {element}")
            return all_elements_with_career
        except AttributeError as error:
            logger.error(f"Searching for HTML element returned error: {error}")

    def extract_from_element(self, element_object: object):
        """

        :param element_object:
        :return:
        """
        pass

    def keywords_search(self, keywords: list):
        """

        :param keywords:
        :return:
        """
        pass
