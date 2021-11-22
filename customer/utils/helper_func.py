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
        token = AuthToken.objects.create(
            user=user, expire=expire(time), type=type)
    except IntegrityError:

        token = AuthToken.objects.get(user=user)
        token.delete()
        token = AuthToken.objects.create(
            user=user, expire=expire(time), type=type)
        # raise serializers.ValidationError({'error': 'email already sent'})
    token.save()
    return token


def authenticate_token(token):

    try:
        Token = AuthToken.objects.get(key=token)
    except AuthToken.DoesNotExist:
        raise exceptions.APIException(
            {'message': 'Invalid Token'}, status.HTTP_403_FORBIDDEN)
    if Token.key != token:
        raise serializers.ValidationError(
            {'error': "token do not match"}, status.HTTP_400_BAD_REQUEST)
    timenow = timezone.now()

    timenow = timenow.replace(tzinfo=pytz.utc)

    if Token.expire < timenow:
        raise serializers.ValidationError(
            {'error': 'Token exp'}, status.HTTP_403_FORBIDDEN)

    return Token.user


def payload(request):
    print('hi')
    try:
        payload = jwt.decode(request,
                             key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        raise AuthenticationFailed({'detail': 'token not provided'})
    return payload