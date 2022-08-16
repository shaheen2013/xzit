
from django.contrib.auth import authenticate
from authentication.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed

from xzit.emails import send_otp


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                username=filtered_user_by_email[0].username, password=os.environ.get('SOCIAL_SECRET'))

            return {
                'id': registered_user.id,
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()
                }

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'first_name' : name,
            'username': generate_username(name), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        
        user = User.objects.create_user(**user)
        user.is_verified = False
        user.auth_provider = provider
        user.save()
         # OTP Send
        if user.email is not None:
            send_otp(user.email, user)
        
        new_user = authenticate(
            username=user.username, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'id': new_user.id,
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }