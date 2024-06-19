"""
Class for fetching a webpage and serve HtML source.
"""
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger


class FetchPage:

    def __init__(self, url):
        self.url: str = url
        logger.info(f"Initiated FetchPage object with url: {self.url}")

    def fetch_with_selenium(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--no-sandbox")

        geckodriver_path = "/snap/bin/geckodriver"
        driver_service = Service(executable_path=geckodriver_path, options=firefox_options)

        try:
            logger.info(f"Trying to install GeckoDriver")
            # The following line should allow installing GeckoDriver if FireFox is not installed.
            # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
            driver = webdriver.Firefox(service=driver_service)
            logger.info(f"GeckDriver installed.")
        except Exception as error:
            logger.error(f"Failed to install GeckoDriver with error:\n{error}")

        try:
            driver.get(url=self.url)
            WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
            logger.info(f"Selenium Fetched {self.url}")
        except Exception as  error:
            logger.error(f"Error trying to fetch {self.url}\nError: {error}")


        page_source = driver.page_source
        driver.quit()
        return page_source

