"""
Scrape websites for jobs postings containing keywords.
"""
from bs4 import BeautifulSoup as bs
import requests

# Set up selenium or BeautifulSoup.
url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url=url)

soup = bs(page.content, "html.parser")


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
jobs_elements = jobs_element.find_all("div", class_="card-content")

# Find jobs with specific keywords.
relevant_jobs = jobs_element.find_all("h2",
                                      string=keywords_search(keyword=["python", "executive"]))

# Iterate through found listings
for job in jobs_elements:
    job_title = job.find("h2", class_="title")
    job_company = job.find("h3", class_="company")
    job_location = job.find("p", class_="location")
    print(f"Title: {job_title.text} \nCompany: {job_company.text} \nLocation: {job_location.text.strip()}\n")

# Look for next type buttons.

# If next button found, Scrape next page for listings and report until no more listings available.
