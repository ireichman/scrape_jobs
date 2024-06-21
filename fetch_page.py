"""
Class for fetching a webpage and serve HtML source.
"""
import requests
import brotli
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger


class FetchPage:
    """
    NEED TO ADD LOGIC FOR DETERMINING STATIC OR DYNAMIC PAGE.
    After determining if the url provided is for a dynamic or static page, this class will fetch this page.
    If the page is dynamic, it will use Selenium.
    If the page is static it will use requests for efficiency.
    """
    def __init__(self, url):
        self.url: str = url
        logger.info(f"Initiated FetchPage object with url: {self.url}")

    def fetch_with_selenium(self):
        """
        Use Selenium to get a web page. Selenium is used because BS4 cannot handle dynamic pages.
        :return: HTML as a string.
        """
        firefox_options = Options()
        # Run selenium without GUI, GPU and sandbox.
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--no-sandbox")

        # For running locally, the path to the gecko dreiver is needed.
        geckodriver_path = "/snap/bin/geckodriver"
        driver_service = Service(executable_path=geckodriver_path)

        try:
            # logger.info(f"Trying to install GeckoDriver")
            # The following line should allow installing GeckoDriver if FireFox is not installed.
            # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
            # logger.info(f"GeckDriver installed.")
            driver = webdriver.Firefox(service=driver_service, options=firefox_options)
        except Exception as error:
            # logger.error(f"Failed to install GeckoDriver with error:\n{error}")
            logger.error(f"Failed to initiate webdriver object with error:\n{error}")
            exit("Cannot continue without webdriver. See error above.")

        try:
            driver.get(url=self.url)
            WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
            logger.info(f"Selenium Fetched {self.url}")
        except Exception as  error:
            logger.error(f"Error trying to fetch {self.url}\nError: {error}")
            exit(f"Could not fetch {self.url} with Selenium.")


        page_source = driver.page_source
        driver.quit()
        return page_source

    def fetch_with_requests(self):
        """
        Requests is the more efficient method for fetching web pages. It should be used by default.
        :return: HTML as string.
        """
        headers = {
            'Accept-Encoding': 'br, gzip, deflate'
        }
        try:
            page = requests.get(url=self.url, headers=headers)
        except Exception as error:
            logger.error(f"Request could not get page. Error: {error}")
            exit(f"Could not fetch {self.url} with Requests.")

        page_decoded = self.check_encoding(web_page=page, website=self.url)
        # Pull the HTML source code from the requests object.
        page_source = page_decoded.content
        return page_source

    def check_encoding(web_page: object, website: str):
        """
        Check the encoding of a requests object. This allows decompressing using Brotli.
        :param website: The URL being decoded.
        :return:
        """
        page_encoding = web_page.encoding
        logger.info(f"Page headers for {website} indicate {page_encoding} compression. Attempting decompression")
        if page_encoding == 'br':
            try:
                decompressed_page = brotli.decompress(web_page.content)
                logger.info(f"Page content for {website} was decompressed successfully using Brotli.")
            except Exception as error:
                logger.error(f"Page headers indicate Brotli compression but decompression failied with error:\n{error}")
        else:
            try:
                decompressed_page = web_page.content
                logger.info(
                    f"Page content for {website} was decoded and/ or decompressed successfully using {page_encoding}.")
            except Exception as error:
                logger.error(f"Could not decode/ decompress {website} which uses {page_encoding}.")
        return decompressed_page