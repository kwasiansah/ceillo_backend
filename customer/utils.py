from django.conf import settings
import jwt
from jwt import exceptions
import pytz
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import Serializer
from customer.models import AuthToken, Customer


def expire(time):
    return timezone.now() + timedelta(seconds=time)


def create_token(user, time, type):
    print(user)
    # integrity error
    token = AuthToken.objects.create(user=user, expire=expire(time), type=type)
    token.save()
    return token


def authenticate_token(user, token):
    try:
        auth_user = user.auth_token
    except Customer.DoesNotExist:
        raise serializers.ValidationError({'error': 'Invalid Token'})
    if auth_user.key != token:
        raise serializers.ValidationError({'error': "token do not match"})
    timenow = timezone.now()

    timenow = timenow.replace(tzinfo=pytz.utc)

    if auth_user.expire < timenow:
        raise serializers.ValidationError({'error': 'Token exp'})

    return user, token


def payload(request):
    print('hi')
    try:
        payload = jwt.decode(request,
                             key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        raise AuthenticationFailed({'detail': 'token not provided'})
    return payload
