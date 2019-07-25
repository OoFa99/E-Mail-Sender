import smtplib
import unicodecsv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

email = 'myMail@gmail.com'
password = 'my password'
subject = 'This is the subject'
message = 'This is my message'


send_to_emails = list()
send_to_emails = [file.rstrip('\n') for file in open('The emails CSV file path')]

files_locations = list()
files_locations = [file.rstrip('\n') for file in open('The attachments paths CSV file path')]

# Connect and login to the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)


for an_email, a_file in zip(send_to_emails, files_locations):
    filename = os.path.basename(a_file)
    attachment = open(a_file, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = an_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))
    # Attach the attachment file
    msg.attach(part)

    # Send the email to this specific email address
    server.sendmail(email, an_email, msg.as_string())


# Quit the email server when everything is done
server.quit()
