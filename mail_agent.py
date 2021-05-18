import smtplib
import os
import imghdr
from email.message import EmailMessage
from pathlib import Path
from senses import speak, listen_speech


def mail_report(from_addr, pwd, to_addr,
                test_file, body, subject,
                cc, attach=False):
    # instance of MIMEMultipart
    msg = EmailMessage()
    # storing the senders email address
    msg['From'] = from_addr
    # storing the receivers email address
    msg['To'] = to_addr
    msg['cc'] = cc
    # storing the subject
    msg['Subject'] = subject
    # attach the body with the msg instance
    msg['body'] = body

    if attach:
        files = os.listdir(test_file)
        for f in files:  # add files to the message
            with open(str(test_file) + '/' + f, 'rb') as m:
                file_data = m.read()
                file_type = imghdr.what(m.name)
                file_name = m.name
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_addr, pwd)
            smtp.send_message(msg)
        speak('mail sent')
