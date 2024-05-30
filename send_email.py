from dotenv import load_dotenv
import os
import smtplib
from loguru import logger
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
        self.email_html: str = f"""\
        <html>
            <body>
                <p>
                {self.email_message}
                </p>
            </body>
        </html>
        """
        self.email_test: str = """"""

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
            title = f"<h3>Jobs from {website}</h3>"
            jobs_paragraph: str = ""
            for job in job_list:
                jobs_paragraph = jobs_paragraph + job.text + "\n"
            email_content_per_site = f"{title}\n{jobs_paragraph}\n\n"
            formatted_email_per_site.append(email_content_per_site)
        formatted_email_all_sites = "\n".join(formatted_email_per_site)
        self.email_message = formatted_email_all_sites
        return self.email_html


