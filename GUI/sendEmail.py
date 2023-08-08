from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from log import *
import ssl
import smtplib

PW_Path = "/home/ailand/GUI_Data/Data/emailPW"
email_sender = "ailandtest40@gmail.com"
#email_receiver = "kuehnast@a-i.land"

def emailTextonly(receiver, subject, text):

    subject = subject
    body  = text
    email_receiver = receiver
    
    try:
        email_password = readPassword()
    except Exception as e:
        eMessage = "Getting E-Mail Passwort failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    # Add body to email
    em.attach(MIMEText(body, "plain"))

    text = em.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def emailWithFile(receiver, subject, text, file):

    subject = subject
    body  = text
    email_receiver = receiver

    try:
        email_password = readPassword()
    except Exception as e:
        eMessage = "Getting E-Mail Passwort failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    # Add body to email
    em.attach(MIMEText(body, "plain"))


    filename = file

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to em and convert em to string
    em.attach(part)

    text = em.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def readPassword():

    f = open(PW_Path, "r")

    return str(f.read())
