"""
Scrape websites for jobs postings containing keywords.
"""
from bs4 import BeautifulSoup as bs
import requests
from loguru import logger
from html_handling import HTML
from threading import Thread as tr


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


if __name__ == "__main__":
    pass


# Read list of websites to scrape. User will populate a text file with a list of sites separated by new line.
websites = list_from_file(file="websites")

# Read list of keywords to look for. User will populate a text file with a list of sites separated by new line.
keywords = list_from_file(file="keywords")

# Pull website.
# url = "https://realpython.github.io/fake-jobs/"
# page = requests.get(url=url)

# Cook soup
job_sites_objects = []
for website in websites[1:]:
    page = requests.get(url=website)
    soup = HTML(html_raw=page, keywords=keywords, website=website) #bs(markup=page.content, features="html.parser")
    job_sites_objects.append(soup)
    # element = job_sites_objects[0].search_elements(element_type="a", text_content="Careers")
    # print("a:\n", job_sites_objects[0].extract_from_element(what_to_extract="href"))

for job_site in job_sites_objects:
    job_site.search_elements(element_type='a', text_content="")
    jobs_list = job_site.keywords_search(keywords=keywords)






# Scrape a website for careers/ jobs/ corporate/ etc.
# for soup in job_sites_objects:
#     careers_link = soup.search_elements(element_type="a", string_text=["career"])

# jobs_elements = jobs_element.find_all("div", class_="card-content")

# Find jobs with specific keywords.
# relevant_jobs = jobs_element.find_all("h2",
#                                       string=lambda text: "python" in text.lower()) # keywords_search(html_string=text, keyword=["python", "executive"]))
#
# relevant_jobs_full_card = [h2_element.parent.parent.parent for h2_element in relevant_jobs]

# Iterate through found listings
# for job in relevant_jobs_full_card:
#     job_title = job.find("h2", class_="title")
#     job_company = job.find("h3", class_="company")
#     job_location = job.find("p", class_="location")
#     job_links = job.find_all(name="a", string=lambda text: "apply" in text.lower())
#     # job_link = job.
#     print(f"Title: {job_title.text} "
#           f"\nCompany: {job_company.text} "
#           f"\nLocation: {job_location.text.strip()} "
#           f"\nApplication link: {job_links[0]['href']}")

# Look for next type buttons.

# If next button found, Scrape next page for listings and report until no more listings available.
