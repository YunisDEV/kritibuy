from flask import Blueprint
import smtplib
from email.message import EmailMessage
import config
email = Blueprint('email', __name__)

smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)


@email.route('/example-email')
def exampleemail():
    msg = EmailMessage()
    msg["Subject"] = "Account Verification"
    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = 'yunisdev.04@gmail.com'
    msg.set_content('Click here to confirm your account')
    msg.add_alternative("""
    <p style="color:red">HELLO</p>
    """, subtype="html")
    smtp.send_message(msg)
    return 'SENT!!!'
