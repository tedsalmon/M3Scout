#!/usr/bin/env python
import smtplib

class Email(object):
    
    EMAIL_ADDY = 'someone@gmail.com'
    
    def __init__(self, ):
        self.SMTP = smtplib.SMTP('smtp.gmail.com', 587)
        self.SMTP.starttls()
        # App specific, GLHF
        self.SMTP.login(self.EMAIL_ADDY, 'somepass')
    
    
    def send_email(self, to, body, ):
        self.SMTP.sendmail(self.EMAIL_ADDY, to, body)
