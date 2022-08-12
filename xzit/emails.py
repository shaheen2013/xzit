from django.core.mail import send_mail
import random
from django.conf import settings

def send_otp(email, user):
       subject = 'Your account verification email'
       otp = random.randint(100000, 999999)
       user.otp = "000000"
       user.is_verified = False
       user.save()
       message = f'Your otp is {otp}'
       email_from = settings.EMAIL_HOST 
       send_mail(subject, message, email_from, [email])
       

def send_reset_otp(email, user):
       subject = 'Your account verification email'
       otp = random.randint(100000, 999999)
       user.reset_pass_otp = otp
       user.save()
       print(user)
       message = f'Your otp is {otp}'
       email_from = settings.EMAIL_HOST 
       send_mail(subject, message, email_from, [email])
       