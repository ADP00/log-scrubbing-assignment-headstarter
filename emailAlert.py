import json
import os
import sys
from pathlib import Path
from loguru import logger

try:
    emailPath = Path(os.getcwd()+"/emails.json")
    with open(str(emailPath), "r") as e:
        emails = json.load(e)
except FileNotFoundError:
    logger.error(f"Emails are not stored in emails.json in the working directory: {os.getcwd()}")
    sys.exit()

SENDER = emails["sender"]
RECEIVER = emails["receiver"]
CC = ""
PASSWORD = emails["password"]

def emailAlert (subject, body):
    import smtplib
    from smtplib import SMTPException
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    receiver = RECEIVER
    sender = SENDER
    cc = CC

    #the receiver emails in the json file must be one string separated by commas
    toEmails = receiver.split(',') + cc.split(',')

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    #if the cc email is an empty string, yahoo will not send the email
    if cc != "":
        message["CC"] = cc

    message.attach(MIMEText(body))
    msg = message.as_string()

    try:
        #the send email in the json must be a yahoo email, and the password must be one generated for third party apps (found in account settings)
        smtpobj = smtplib.SMTP("smtp.mail.yahoo.com", 587)
        #smtpobj.set_debuglevel(1)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(sender, PASSWORD)
        smtpobj.sendmail(sender, toEmails, msg)
        smtpobj.close()

    except SMTPException:
        logger.exception(f"Unable to send email. Failed to send from {sender} to {', '.join(toEmails)}.")
