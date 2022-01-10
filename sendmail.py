import payload
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication

class Gmail:
    def __init__(self):
        self.user, self.password = payload.from_txt('creds.txt')
        self.server = smtplib.SMTP(host= 'smtp.gmail.com', port= 587)
        self.server.starttls()
        self.server.login(self.user, self.password)
        self.msg = MIMEMultipart()
        self.msg['From'] = self.user

    def to(self, recipient):
        self.msg['To'] =  recipient

    def subject(self, topic):
        self.msg['Subject'] = topic

    def message(self, body):
        self.msg.attach(MIMEText(body, 'plain'))

    def attach(self, attachment):
        file_name = basename(attachment)
        with open(attachment, 'rb') as file:
            file_content = file.read()
            part = MIMEApplication(file_content, Name=file_name)
        part['Content-Disposition'] = f'attachment; filename={file_name}'
        self.msg.attach(part)

    def send(self):
        self.server.send_message(self.msg)
        self.server.quit()

def buildGmail(variable_list):
    to, subject, message, attach = variable_list
    g = Gmail()
    g.to(to)
    g.subject(subject)
    g.message(message)
    g.attach(attach)
    g.send()