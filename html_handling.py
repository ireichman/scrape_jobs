"""

"""
from bs4 import BeautifulSoup as bs
import requests
from loguru import logger


class HTML:

    def __init__(self, html_raw):
        self.html = bs(markup=html_raw.content, features="html.parser")

    def search_elements(self, element_type: str, string_text: list, element_attribute: str = None):
        """
        Find HTML elements who's string match any of the strings in string_text. Optionally, Specify a different HTML
        attribute that string_text should match.
        :param element_type: Specify what type of element to search for.
        :param string_text: A list of strings to search for in the html 'string' attribute (unless element_attribute is
        specified).
        :param element_attribute: Optionally, specify an HTML attribute to search in instead of 'string'.
        :return: ???
        """
        pass

    def keywords_search(self, keywords: list):
        """

        :param keywords:
        :return:
        """
        pass
