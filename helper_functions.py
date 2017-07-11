import os.path as path
from os import listdir
from email.mime.text import MIMEText
import smtplib


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]


def send_email(sender, password, receivers, subject, message="", server="smtp-mail.outlook.com", protocol=587):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(receivers)
    server = smtplib.SMTP(server, protocol)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receivers, msg.as_string())
    server.quit()


def input_true_or_false(user_input, true_cond={"y"}):
    return True if user_input in true_cond else False
