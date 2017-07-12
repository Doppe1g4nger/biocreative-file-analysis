import os.path as path
from email.mime.text import MIMEText
import smtplib
import os


def get_all_files(fpath):
    return [path.join(fpath, f) for f in os.listdir(fpath) if path.isfile(path.join(fpath, f))]


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


def replace_pathvar_with_environ(string):
    path_var_start = string.find("$")
    if path_var_start != -1:
        path_slice = string[path_var_start + 1:string.find("/", path_var_start)]
    else:
        return string
    try:
        path_replacement = os.environ[path_slice]
        return replace_pathvar_with_environ(string.replace(path_slice, path_replacement))
    except:
        raise