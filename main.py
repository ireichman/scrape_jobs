"""
Scrape websites for jobs postings containing keywords.
"""
from bs4 import BeautifulSoup as bs
import requests
from loguru import logger

# Set up selenium or BeautifulSoup.
url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url=url)
soup = bs(markup=page.content, features="html.parser")


def list_from_file(file: str):
    """
    Read a text file and break text in to a list of words by new line.
    Designed for 'keywords' and 'websites' but can take any file name or path.
    :param file: Specify 'keywords' or 'websites'. Otherwise, give it the full file name and path if not in the base folder.
    :return: List of strings.
    """
    logger.info(f"Reading {file}")
    if file == "keywords":
        file = "keywords.txt"
    elif file == "websites":
        file = "websites.txt"
    else:
        file = file
    try:
        with open(file=file, mode='r') as file_words:
            words_raw = file_words.read()
    except Exception as error:
        logger.error(f"Attempting to read {file} returned an error:\n{error}")
    words_list = words_raw.splitlines()
    words = [word.lower() for word in words_list]
    logger.info(f"Reading {file} returned the following list:\n{words}")
    return words


def search_elements(element_type: str, string_text: str):
    """
    Find elements of specific type and
    :param element_type:
    :param string_text:
    :return:
    """
    ""


def keywords_search(html_string: str, keywords: list):
    """
    Search for keywords in a string.
    :param keywords: List of keywords.
    :param html_string: string to search in.
    :return: boolean.
    """
    for keyword in keywords:
        if keyword in html_string.lower():
            return True
        else:
            continue
    return False
# Read list of websites to scrape. User will populate a text file with a list of sites separated by new line.

# Read list of keywords to look for. User will populate a text file with a list of sites separated by new line.

# Scrape a website for careers/ jobs/ corporate/ etc.
jobs_element = soup.find(id="ResultsContainer")
# jobs_elements = jobs_element.find_all("div", class_="card-content")

# Find jobs with specific keywords.
relevant_jobs = jobs_element.find_all("h2",
                                      string=lambda text: "python" in text.lower()) # keywords_search(html_string=text, keyword=["python", "executive"]))

relevant_jobs_full_card = [h2_element.parent.parent.parent for h2_element in relevant_jobs]

# Iterate through found listings
for job in relevant_jobs_full_card:
    job_title = job.find("h2", class_="title")
    job_company = job.find("h3", class_="company")
    job_location = job.find("p", class_="location")
    job_links = job.find_all(name="a", string=lambda text: "apply" in text.lower())
    # job_link = job.
    print(f"Title: {job_title.text} "
          f"\nCompany: {job_company.text} "
          f"\nLocation: {job_location.text.strip()} "
          f"\nApplication link: {job_links[0]['href']}")

# Look for next type buttons.

# If next button found, Scrape next page for listings and report until no more listings available.
