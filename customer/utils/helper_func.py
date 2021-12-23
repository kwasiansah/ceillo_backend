from django.shortcuts import render
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
import jwt
import pytz
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from customer.models import AuthToken, Customer
from django.db.utils import IntegrityError


def expire(time):
    return timezone.now() + timedelta(seconds=time)


def create_token(user, time, type):
    print(user)
    # integrity error
    try:
        token = AuthToken.objects.create(user=user, expire=expire(time), type=type)
    except IntegrityError:

        token = AuthToken.objects.get(user=user)
        token.delete()
        token = AuthToken.objects.create(user=user, expire=expire(time), type=type)
        # raise serializers.ValidationError({'error': 'email already sent'})
    token.save()
    return token


# check if tokens are deleted after authentication in view or here


def authenticate_token(token):

    try:
        Token = AuthToken.objects.get(key=token)
    except AuthToken.DoesNotExist:
        raise exceptions.APIException(
            {"message": "Invalid Token"}, status.HTTP_403_FORBIDDEN
        )
    if Token.key != token:
        # change this to invalid token later on
        raise serializers.ValidationError(
            {"error": "token do not match"}, status.HTTP_400_BAD_REQUEST
        )
    timenow = timezone.now()

    timenow = timenow.replace(tzinfo=pytz.utc)

    if Token.expire < timenow:
        raise serializers.ValidationError(
            {"error": "Token exp"}, status.HTTP_403_FORBIDDEN
        )

    return Token.user


def payload(request):
    print("hi")
    try:
        payload = jwt.decode(
            request, key=settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"]
        )
    except jwt.exceptions.DecodeError:
        raise AuthenticationFailed({"detail": "token not provided"})
    return payload


def password_reset_email(user, token):
    link = f"https://ceillo.netlify.app/password-reset-confirm/{token}/"

    subject = "Your password reset "

    sender = settings.EMAIL_HOST_USER
    # remember to make this link dynamic
    logo_link = "https://ceillo-app.herokuapp.com/media/default/ceillo.svg"
    to = [user.email]

    html_content = render_to_string(
        "password_reset_email.html",
        {
            "first_name": user.first_name,
            "email": user.email,
            "link": link,
            "logo_link": logo_link,
        },
    )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, sender, to)
    email.attach_alternative(html_content, "text/html")
    email.send()
    return user.email.upper()


def generic_email(user, subject, link, sender, to, template_name, template_data):
    html_content = render_to_string(template_name, template_data)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, sender, to)
    email.attach_alternative(html_content, "text/html")
    email.send()
    return user.email.upper()
