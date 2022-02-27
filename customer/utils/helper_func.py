from datetime import timedelta

import jwt
import pytz
from customer.models import AuthToken
from customer.utils import constant
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.utils import IntegrityError
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from .exceptions import UnprocessableEntity

User = get_user_model()


def expire(time):
    return timezone.now() + timedelta(seconds=time)


def create_token(user, time, type):
    print(user)
    # integrity error
    try:
        token = AuthToken.objects.create(
            user=user, expire=expire(time), type=type
        )
    except IntegrityError:

        token = AuthToken.objects.get(user=user)
        token.delete()
        token = AuthToken.objects.create(
            user=user, expire=expire(time), type=type
        )
    token.save()
    return token


# check if tokens are deleted after authentication in view or here


def authenticate_token(token):

    try:
        Token = AuthToken.objects.get(key=token)
    except AuthToken.DoesNotExist:
        raise AuthenticationFailed(
            {"message": "Your Verification Link Is Invalid"},
            status.HTTP_401_UNAUTHORIZED,
        )
    timenow = timezone.now()

    timenow = timenow.replace(tzinfo=pytz.utc)

    if Token.expire < timenow:
        raise AuthenticationFailed(
            {"message": "Your Verification Link Has Expired"},
            status.HTTP_401_UNAUTHORIZED,
        )

    return Token.user


def payload(request):
    print("hi")
    try:
        payload = jwt.decode(
            request,
            key=settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithms=["HS256"],
        )
    except jwt.exceptions.DecodeError:
        raise AuthenticationFailed({"detail": "token not provided"})
    return payload


def generic_email(
    user, subject, link, sender, to, template_name, template_data
):
    html_content = render_to_string(template_name, template_data)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, sender, to)
    email.attach_alternative(html_content, "text/html")
    email.send()
    return user.email.upper()


def password_reset_email(user, token):
    link = f"https://ceillo.netlify.app/password-reset-confirm/{token}/"
    subject = "Your password reset "
    sender = settings.EMAIL_HOST_USER
    # remember to make this link dynamic
    logo_link = constant.LOGO_URL
    to = [user.email]
    template_name = constant.PASSWORD_RESET_TEMPLATE
    template_data = {
        "first_name": user.first_name,
        "email": user.email,
        "link": link,
        "logo_link": logo_link,
    }
    email = generic_email(
        user,
        subject,
        link,
        sender,
        to,
        template_name,
        template_data,
    )
    return email


def send_verify_email(user, request=None):
    logo_link = constant.LOGO_URL
    token = create_token(user, 60 * 5, "verify")
    link = f"https://ceillo.netlify.app/verify-email/{token}/"
    print(token)
    temp_data = {
        "email": user.email,
        "first_name": user.first_name,
        "link": link,
        "logo_link": logo_link,
    }
    generic_email(
        user,
        constant.VERIFY_EMAIL_SUBJECT,
        link,
        settings.EMAIL_HOST_USER,
        [user.email],
        constant.VERIFY_EMAIL_TEMPLATE,
        temp_data,
    )
    return user.email


def validate_email(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as e:
        return None

    if user.verified_email:
        raise UnprocessableEntity(
            {"message": "Email Already Exists"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        email = send_verify_email(user, request)

        return email.upper()
