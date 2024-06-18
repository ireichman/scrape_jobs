# Job Scraper.

## Purpose:
Is there a dream job for you out there? Would you like to be a Lion Tamer but stuck doing accounting?  
This app allows you to check relevant employers for specific jobs on a regular basis. When jobs are found \ 
they will be emailed to you. So stop checking these postings obsessively (or even lackadaisically) and just \
check your email!

## Description:
Given a list of websites and a list of keywords that could be in a the job title/ description. \
The program will make a list of relevant job postings on those websites and email a list of 
relevant jobs with a link for applying to them.
THIS APP IS IN A VERY EARLY STAGE OF DEVELOPMENT. Use at your own risk.


## To-Do/ Roadmap:
* Add text option to email.
* ~~Email title shows the number of websites scraped not jobs found.~~
* ~~Check why sending an email when Canonical cannot be decoded gives an empty email.~~ 
* Finesse message formatting. (~~Show links in newline~~, better job titles, user's name.)
* Switch to DB instead of text files.
* Add logic for scraping once, filtering once, then emailing each user the relevant jobs.
* Add logic for finding job listings on a website instead of requiring specific URL.
* Improve listing search. (Check that results are actually jobs and relevant links. Maybe check if 'href' is relevant?)
* Add verificaton that URL is completer with scheme and path.
* Make a webapp:
    * Design site
    * Add secure user login.
    * Give users ability to edit sites, keywords, email address.
    * 
  