from dotenv import load_dotenv
import os
import smtplib
from loguru import logger
from urllib.parse import urlparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv("secrets.env")
FROM_ADDR: str = os.getenv("FROM_ADDR")
PWD: str = os.getenv("PWD_YAHOO")


class Email:

    def __init__(self, to_address: str, jobs: dict):
        self.from_address: str = FROM_ADDR
        self.to_address: str = to_address
        self.jobs: dict = jobs
        self.email_message: str = ""

        self.email_text: str = """"""

    def send_email(self):
        with smtplib.SMTP(host="smtplib.mail.yahoo.com", port=587) as emai_connection:
            emai_connection.ehlo()
            emai_connection.starttls()
            emai_connection.login(user=self.to_address, password=PWD)
            try:
                emai_connection.sendmail(from_addr=self.from_address,
                                         to_addrs=self.to_address,
                                         msg=self.email_message)
                logger.info(f"Sent email to {self.to_address}")
                return True
            except Exception as error:
                logger.error(f"Sending email to {self.email_message} failed with error:\n{error}")
                return False

    def format_email(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Jobs Digest. {len(self.jobs)} new jobs found."
        message["From"] = self.from_address
        message["To"] = self.to_address
        formatted_email_per_site = []
        for website, job_list in self.jobs.items():
            website_parts = self.trim_website_string(website)
            title = f"<h3>Jobs from {website_parts[1]}</h3>"
            jobs_paragraph: str = ""
            for job in job_list:
                job_url = job["href"]
                if "https" not in job_url:
                    job_url = website_parts[0] + "://" + website_parts[1] + job_url

                jobs_paragraph = jobs_paragraph + f'<a href="{job_url}">{job.text}</a>' + "\n"
            email_content_per_site = f"{title}\n{jobs_paragraph}\n\n"
            formatted_email_per_site.append(email_content_per_site)
        formatted_email_all_sites = "\n".join(formatted_email_per_site)
        self.email_message = formatted_email_all_sites
        self.create_html_email()
        return self.email_message

    def create_html_email(self):
        self.email_html: str = f"""\
        <html>
            <body>
                <p>
                {self.email_message}
                </p>
            </body>
        </html>
        """
        return self.email_html

    def create_text_email(self):
        pass

    def trim_website_string(self, website):
        """
        Takes a URL string and splits it to scheme, domain, and the rest of the URL.
        :param website: String that contains URL.
        :return: Tuple with URL parts
        """
        parse_url = urlparse(url=website)
        url_scheme = parse_url.scheme
        url_domain = parse_url.netloc
        url_path = parse_url.path
        return url_scheme, url_domain, url_path


