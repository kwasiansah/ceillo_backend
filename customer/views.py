
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import EmailMessage
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from datetime import timedelta
from django.contrib.auth import login, logout
from django.core.checks import messages
from django.db.models import query
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CreateCustomerSerializer, CustomerPasswordChangeSerializer, CustomerUserPasswordResetConfirmSerializer,  ListCustomerSerializer, MerchantSerializer, MyTokenObtainPairSerializer,  RetrieveCustomerSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Customer, Merchant
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin

from rest_framework.authentication import authenticate
from rest_framework.renderers import BrowsableAPIRenderer
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from .utils import create_token, authenticate_token, payload


# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

# @action(detail=True, methods=['PATCH'])
# def set_password(self, request, pk=None):
#     user = self.get_object()
#     serializer = UserSerializer(data=request.data, patch=True)
#     if serializer.is_valid():
#         user.set_password(serializer.validated_data['password'])
#         user.save()
#         return Response({'status': 'password set'})
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomerViewSet(viewsets.ModelViewSet):
#     serializer_class = CustomerSerializer
#     queryset = Customer.objects.all()

class CustomerList(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = ListCustomerSerializer
    lookup_field = 'custmer_id'


class CustomerRetrieve(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = RetrieveCustomerSerializer
    lookup_field = 'customer_id'


class CustomerCreate(CreateAPIView, ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CreateCustomerSerializer


class MerchantViewSet(viewsets.ModelViewSet):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()
# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    queryset = Customer.objects.all()
    serializer = ListCustomerSerializer(queryset, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


def g(request):
    for i in dir(request):
        print(i)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    serializer = RetrieveCustomerSerializer(user)
    data = {
        'data': serializer.data,
        'message': 'detailed view results'
    }
    return Response(data)


@ api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_update(request):
    data = payload(str(request.auth))
    try:
        queryset = Customer.objects.get(customer_id=data['user_id'])
    except Customer.DoesNotExist:
        data = {
            'message': 'user does not exit'
        }
        return Response(data, status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        serializer = RetrieveCustomerSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            data = {
                'status': 'okay',
                'data': serializer.data,
                'message': 'detailed view results'
            }
            return Response({"data": "invalid data to update"})
    else:
        serializer = RetrieveCustomerSerializer(
            queryset, data=request.data, partial=True)
        # remove the raise_exception to output the response data
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"data": "invalid data to patch"})
    return Response(serializer.data)


@ api_view(['POST'])
def user_create(request):
    serializer = CreateCustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print(serializer.validated_data)
        print(serializer.data)
        data = {
            'data': serializer.data,
            'token': serializer.validated_data['token'],
            'message': 'sign up successfull',
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request, first_name):
    data = payload(str(request.auth))
    print(data['user_id'])
    try:
        queryset = Customer.objects.get(customer_id=data['user_id'])
    except Customer.DoesNotExist:
        return Response(data='user does not exit')
    serilizer = RetrieveCustomerSerializer(queryset)
    queryset.delete()
    return Response(serilizer.data)


@ api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request, first_name):
    data = payload(str(request.auth))
    print(data['user_id'])
    try:
        queryset = Customer.objects.get(customer_id=data['user_id'])
    except Customer.DoesNotExist:
        return Response(data='user does not exit')
    serializer = CustomerPasswordChangeSerializer(queryset, data=request.data)
    print(serializer)
    print('it got here')
    if serializer.is_valid(raise_exception=True):
        print('befor save')
        serializer.save()
    print('befor response')
    # TODO: remove the serailizer.data and create custom response
    # TODO: make the password field in the serializer class write_only

    return Response(serializer.data)

# TODO: i must change the first_name parameter to email because it would accept email

# @api_view(['POST'])


@ api_view(('GET',))
@ renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def user_password_reset(request, first_name):
    # sends the email
    time = 60 * 50
    data = payload(str(request.auth))
    try:
        user = Customer.objects.get(customer_id=data['user_id'])
    except Customer.DoesNotExist:
        return Response(data='user does not exit')

    token = create_token(user, time, 'email')
    print(token)
    link = request.build_absolute_uri(
        f'/auth/password-rest-confirm/{token.key}/')
    print(link)
    subject = 'your password reset token '
    message = f'hello {first_name} follow this link to reset your password {link}'
    sender = settings.EMAIL_HOST_USER
    # TODO: the to would be changed to request.data
    to = ['kwasiansahasare@gmail.com']
    send_mail(subject, message, sender, to)

    return Response({'reset': 'password reset email sent'})
    """
    this is where the email is sent
    so it would take a post of the users email adderess and
    send the mail
    with the token
    a new serializer class would be create here
    """


def user_password_reset_done(request, first_name):
    """ confirms the sent email with the token
        i think this view would be implemented in the front end
    """
    pass


@ api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_password_reset_confirm(request, token):
    data = payload(str(request.auth))
    print(data['user_id'])
    try:
        user = Customer.objects.get(customer_id=data['user_id'])
    except Customer.DoesNotExist:
        return Response(data='user does not exit')

    auth_user = authenticate_token(user, token)

    serializer = CustomerUserPasswordResetConfirmSerializer(
        instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'password': "password successfuly reset"})
    return Response({'password': 'password reset not valid'})
    """
    this view would confirm the token and
    and give a form for the new password
    meaning a new serializer class would be created here
    """


def user_password_reset_complete(request, first_name):
    """ confirms the password reset but  it would be done by the front end """
    pass
