from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CreateCustomerSerializer, CustomerPasswordChangeSerializer, CustomerUserPasswordResetConfirmSerializer,  ListCustomerSerializer, MerchantSerializer, MyTokenObtainPairSerializer,  RetrieveCustomerSerializer
from rest_framework.response import Response
from .models import Customer, Merchant
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from django.core.mail import send_mail
from django.conf import settings
from .utils import create_token, authenticate_token


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
    data = {
        'data': [serializer.data],
        'message': 'list of all customers'
    }
    return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    serializer = RetrieveCustomerSerializer(user)
    data = {
        'data': serializer.data,
        'message': 'customer details'
    }
    return Response(data, status.HTTP_200_OK)


@ api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    if request.method == "PUT":
        serializer = RetrieveCustomerSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            data = {
                'status': 'okay',
                'data': serializer.data,
                'message': "invalid data to update"
            }
            return Response(data, status.HTTP_406_NOT_ACCEPTABLE)
    else:
        serializer = RetrieveCustomerSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            data = {
                'status': 'okay',
                'data': serializer.data,
                'message': "invalid data to patch"
            }
            return Response(data, status.HTTP_406_NOT_ACCEPTABLE)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def user_create(request):
    serializer = CreateCustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {
            'data': serializer.data,
            'token': serializer.validated_data['token'],
            'message': 'sign up successfull',
        }
        return Response(data, status=status.HTTP_201_CREATED)
    data = {
        'errors': serializer.errors,
        'message': 'sign up unsuccessfull'
    }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request):
    user = request.user
    user.delete()
    data = {
        'message': 'customer successfully deleted'
    }
    return Response(data, status.HTTP_201_CREATED)


@ api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request):
    user = request.user
    serializer = CustomerPasswordChangeSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
    data = {
        'message': " password successfully changed"
    }
    return Response(data, status.HTTP_200_OK)


@ api_view(('GET',))
@ renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def user_password_reset(request):

    timeout = 60 * settings.EMAIL_RESET_TOKEN_TIMEOUT_MIN

    user = request.user
    token = create_token(user, timeout, 'email')
    # TODO: this link would be linked to a part of the front end
    link = request.build_absolute_uri(
        f'/auth/password-reset-confirm/{token.key}/')
    subject = 'your password reset token '
    message = f'hello {user.first_name} follow this link to reset your password {link}'
    sender = settings.EMAIL_HOST_USER
    # TODO: the to would be changed to request.data
    to = ['kwasiansahasare@gmail.com']
    # send_mail(subject, message, sender, to)
    print(link)
    return Response({'reset': 'password reset email sent'})


@ api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_password_reset_confirm(request, token):
    user = request.user
    data = {'message': "password successfuly reset"}
    auth_user = authenticate_token(user, token)
    serializer = CustomerUserPasswordResetConfirmSerializer(
        instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        user.auth_token.delete()
        return Response(data, status.HTTP_200_OK)
    data['message'] = 'password reset not valid'
    return Response(data, status.HTTP_400_BAD_REQUEST)