from django.core.mail import send_mail
import random
from django.conf import settings

import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, body, email_from, recipient_list):
        self.subject = subject
        self.body = body
        self.email_from = email_from
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run (self):
       send_mail(self.subject, self.body, self.email_from, self.recipient_list)

def send_mail_async(subject, body, email_from, recipient_list):
    EmailThread(subject, body, email_from, recipient_list).start()



def send_otp(email, user):
       subject = 'Your account verification email'
       otp = random.randint(100000, 999999)
       user.otp = otp
       user.is_verified = False
       user.save()
       message = f'Your otp is {otp}'
       email_from = settings.EMAIL_HOST_USER 
       send_mail_async(subject, message, email_from, [email])
       

def send_reset_otp(email, user):
       subject = 'Your account verification email'
       otp = random.randint(100000, 999999)
       user.reset_pass_otp = otp
       user.save()
       print(user)
       message = f'Your otp is {otp}'
       email_from = settings.EMAIL_HOST_USER 
       send_mail_async(subject, message, email_from, [email])
       