import smtplib, codecs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json

class EmailSender():
    
    def __init__(self, sender, password, receiver, host = 'smtp.gmail.com', port= 587):
        pass

        self.s = smtplib.SMTP(host = host, port = port)
        self.s.starttls()
        self.s.login(sender, password)

        self.sender = sender
        self.receiver = receiver

        self.template_email = "ui/resources/email_template/report_template.html"
        self.email_to_send  = "ui/resources/email_template/email_send.html"

    def sendMsg(self, subject, body):

        

        with open(self.template_email,'r')as e:
            change_email = e.readlines()

        new_email = []
        for line in change_email:
            if "&lt;&lt;&lt;None&gt;&gt;&gt;" in line:
                line = line.replace(r"&lt;&lt;&lt;None&gt;&gt;&gt;",body.replace("\n","&#10;"))
            new_email.append(line)

        with open(self.email_to_send,'w') as w:
            for line in new_email:
                w.write(line)

        code_html = codecs.open(self.email_to_send, 'r')
        text = code_html.read()

        msg = MIMEMultipart()
        msg = MIMEMultipart('alternative')

        msg['From']     = self.sender
        msg['To']       = self.receiver
        msg['Subject']  = subject

        msg.attach(MIMEText(text, 'html'))

        self.s.sendmail(self.sender,self.receiver,msg.as_string())

        del msg

def jsonDump(jsonFile, data):
    with open(jsonFile, "w") as write_file:
        json.dump(data, write_file, separators=(", ", ": "), indent = 4, sort_keys = False)

def jsonRead(jsonFile):
    with open(jsonFile, "r") as read_file:
        return json.load(read_file)