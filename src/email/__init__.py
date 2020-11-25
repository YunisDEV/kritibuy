import smtplib
from email.message import EmailMessage
import config

smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)


def send_mail(Subject='TEST', From=config.EMAIL_ADDRESS, To=config.TEST_EMAIL_ADDRESS, Content='', HTML=None):
    try:
        msg = EmailMessage()
        msg["Subject"] = Subject
        msg["From"] = From
        msg["To"] = To
        msg.set_content(Content)
        if HTML:
            msg.add_alternative(HTML, subtype="html")
        smtp.send_message(msg)
        return True
    except Exception as e:
        print(e)
        return False
