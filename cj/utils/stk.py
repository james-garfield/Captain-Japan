# Send PDFs, MOBI to Kindle by email

import smtplib

from os.path import basename

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formatdate

from cj.objects.book import Book


class NoEmailException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class KindleConn:
    def __init__(self, email_to: str, email_from: str, password_from: str, book: Book) -> None:
        self.email_to = email_to
        self.email_from = email_from
        self.password = password_from
        self.book = book

    def send(self):
        """
        Send the Novel to a kindle. Will raise exceptions if there is no email_from or email, 
        or no location in the novel path.
        """
        if self.email_to is None:
            raise NoEmailException("No email_to address provided.")
        if self.email_from is None:
            raise NoEmailException("No email_from email address provided.")
        if self.book.location is None:
            raise ValueError("No location provided for the novel.")

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.email_from
        message["To"] = self.email_to
        # Default subject
        message["Subject"] = "Your Novel"
        # If there is a title in the Book then add it to the subject
        if self.book.title:
            message['Subject'] += f" - {self.book.title}"
        message['Date'] = formatdate(localtime=True)
        message.attach(MIMEText("Hi from Captain Japan, here is your requested novel."))
        # Open and read file
        with open(self.book.location, 'rb') as file:
            attachment = MIMEApplication(
                file.read(),
                Name=basename(self.book.location)
            )
        # Add file to message
        attachment["Content-Disposition"] = f"attachment; filename={basename(self.book.location)}"
        message.attach(attachment)

        # Send the message via local SMTP server
        session = smtplib.SMTP('smtp.gmail.com', 587)
        # Login with security
        session.starttls()
        # Use the email_from and password
        session.login(self.email_from, self.password)
        
        # Send the message
        session.sendmail(self.email_from, self.email_to, message.as_string())
        session.quit()


if __name__ == "__main__":
    # Test sending a book
    loc = r"C:\Users\jorda\Downloads\Overlord - Vol. 3 - The Bloody Valkyrie by Maruyama Kugane [Maruyama Kugane] (z-lib.org).pdf"
    book = Book(title="The Little Book of Stoicism", location=loc)
    kindle_con = KindleConn("jordanmcastro@outlook.com", "jordan@grupojvm.com", "Superboy$", book)
    kindle_con.send()
