import smtplib
from email.message import EmailMessage
import config
from jinja2 import Template as HTMLTemplate

smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)


def send_mail(Subject='TEST', From=config.EMAIL_ADDRESS, To=config.TEST_EMAIL_ADDRESS, Content='', HTML=None, Template={}):
    try:
        msg = EmailMessage()
        msg["Subject"] = Subject
        msg["From"] = From
        msg["To"] = To
        msg.set_content(Content)
        if HTML:
            msg.add_alternative(HTML, subtype="html")
        elif Template:
            temp_name = Template["name"]
            temp_data = Template["data"]
            temp_code = open(f'src/email/templates/{temp_name}.html','rt').read()
            temp = HTMLTemplate(temp_code)
            temp_html = temp.render(data=temp_data)
            msg.add_alternative(temp_html, subtype="html")
        smtp.send_message(msg)
        return True
    except Exception as e:
        print(e)
        return False
