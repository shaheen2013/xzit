from django.core.mail import send_mail
import random
from django.conf import settings
from django.template.loader import render_to_string    

def send_otp(email, user):
       subject = 'Your account verification email'
       otp = random.randint(100000, 999999)
       user.otp = otp
       user.is_verified = False
       user.save()
       message_html = render_to_string('email/otp_email.html', {'otp': otp})
       email_from = settings.EMAIL_HOST_USER 
       send_mail(subject, message='', from_email=email_from, recipient_list=[email], html_message=message_html)
       
def send_reset_otp(email, user):
       subject = 'Your account verification email'
       otp = random.randint(100000, 999999)
       user.reset_pass_otp = otp
       user.save()
       message = render_to_string('email/otp_email.html', {'otp': otp})
       email_from = settings.EMAIL_HOST_USER 
       send_mail(subject, message, email_from, [email])
       