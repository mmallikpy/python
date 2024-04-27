# This script can send email using attachment "text file"

import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from_addr = "fromAddress@gmail.com"
to_addr = 'ToAddress@gmail.com'
subject = "Email send with attachment"
content = "Tst email with attachment"

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject
body = MIMEText(content, 'plain')
msg.attach(body)

filename = 'output.txt'

with open(filename, 'r') as f:
    attachment = MIMEApplication(f.read(), Name=basename(filename))
    attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))

msg.attach(attachment)
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(from_addr, "Your API Key")
server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
