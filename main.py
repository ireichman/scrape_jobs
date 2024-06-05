"""
Scrape websites for jobs postings containing keywords.
"""
import requests
from loguru import logger
from html_handling import HTML
from send_email import Email


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

# Cook soup
job_sites_objects = []
for website in websites[1:]:
    try:
        page = requests.get(url=website)
        page_encoding = page.encoding
    except Exception as error:
        logger.error(f"Request could not get page. Error: {error}")
        continue
    try:
        logger.info(f"Trying to decode {website} page with {page_encoding} to make sure it's valid.")
        page.content.decode(page_encoding)
        logger.info(f"Successfully decoded {website} with {page_encoding}")
    except Exception as error:
        logger.error(f"Error decodidng {website}. Error info.:\n{error}")
        continue

    soup = HTML(html_raw=page, keywords=keywords, website=website)
    job_sites_objects.append(soup)

jobs_dict = {}
for job_site in job_sites_objects:
    job_site.search_for_elements(element_type='a', text_content="")
    jobs_list = job_site.keywords_search(keywords=keywords)
    jobs_dict[job_site.website] = jobs_list


email = Email(to_address="xxx@xxx.com", jobs=jobs_dict)
email_html = email.format_email()
print("HTML: ", email.email_html)
email.send_email()
