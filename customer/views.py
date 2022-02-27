from .utils.helper_func import validate_email
from customer.utils.helper_func import send_verify_email
from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, status
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import AuthToken, Customer, Merchant
from .permissions import IsLoggedOut
from .serializers import (
    CreateCustomerSerializer,
    CustomerLogoutSerializer,
    CustomerPasswordChangeSerializer,
    CustomerUserPasswordResetConfirmSerializer,
    MerchantSerializer,
    MyTokenObtainPairSerializer,
    RetrieveCustomerSerializer,
    UpdateCustomerSerializer,
)
from .utils import constant
from .utils.helper_func import (
    authenticate_token,
    create_token,
    password_reset_email,
)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    ),
)
class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsLoggedOut])
def user_list(request):
    queryset = Customer.objects.all()
    serializer = RetrieveCustomerSerializer(queryset, many=True)
    data = {"data": serializer.data, "message": "list of all customers"}
    return Response(data, status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsLoggedOut])
def user_detail(request):
    user = request.user
    serializer = RetrieveCustomerSerializer(user, context={"request": request})
    data = {"data": serializer.data, "message": "customer details"}
    return Response(data, status.HTTP_200_OK)


@swagger_auto_schema(
    methods=["put", "patch"], request_body=UpdateCustomerSerializer
)
@api_view(["PUT", "PATCH"])
@parser_classes([MultiPartParser, JSONParser])
@permission_classes([IsAuthenticated, IsLoggedOut])
def user_update(request):
    user = request.user
    if request.method == "PUT":
        serializer = UpdateCustomerSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        else:
            data = {
                "data": serializer.data,
                "message": "invalid data to update",
            }
            return Response(data, status.HTTP_406_NOT_ACCEPTABLE)
    else:
        serializer = UpdateCustomerSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        else:
            data = {
                "data": serializer.data,
                "message": "invalid data to patch",
            }
            return Response(data, status.HTTP_406_NOT_ACCEPTABLE)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["POST"])
def user_create(request):

    email = validate_email(request)
    if email:
        return Response(
            {"message": f"An Email Has Been Sent To {email}"},
            status.HTTP_200_OK,
        )
    serializer = CreateCustomerSerializer(
        data=request.data, context={"request": request}
    )
    # when raise exception is true test password match needs change
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        email = send_verify_email(serializer.instance, request)
        data = {"message": f"An Email Has Been Sent To {email}"}
        return Response(data, status=status.HTTP_201_CREATED)
    # message = serializer.errors['email']
    # this part is not been accessed
    data = {
        **serializer.errors,
        "message": "Sign Up Unsuccessfull",
    }

    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsLoggedOut])
def user_delete(request):
    user = request.user
    user.delete()
    data = {"message": "Account Deleted"}
    return Response(data, status.HTTP_201_CREATED)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["old_password", "password", "password2"],
        properties={
            "old_password": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "password2": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsLoggedOut])
def password_change(request):
    user = request.user
    serializer = CustomerPasswordChangeSerializer(user, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        data = {"message": "Password Successfully Changed"}
        return Response(data, status.HTTP_200_OK)
    return Response({"message": "Invalid Inputs"}, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(["POST"])
def user_password_reset(request):
    timeout = 60 * settings.EMAIL_RESET_TOKEN_TIMEOUT_MIN
    try:
        user = Customer.objects.get(email=request.data["email"])
    except Customer.DoesNotExist:
        data = {"message": "Account Not Found"}
        raise exceptions.NotFound(data, status.HTTP_404_NOT_FOUND)
    token = create_token(user, timeout, "email")
    email = password_reset_email(user, token)
    data = {
        "message": f"An Email Has Been Sent To {email}",
    }
    return Response(data, status.HTTP_200_OK)


@api_view(["POST"])
def user_password_reset_confirm(request):
    token = request.data.get("token", False)
    if not token:
        raise exceptions.NotFound(
            {"message": "Token Not Found"}, status.HTTP_404_NOT_FOUND
        )
    data = {"message": "Password Reset Successfull"}
    user = authenticate_token(token)
    serializer = CustomerUserPasswordResetConfirmSerializer(
        instance=user, data=request.data
    )
    if serializer.is_valid():
        serializer.save()
        user.auth_token.delete()
        return Response(data, status.HTTP_200_OK)
    data["message"] = "Password Reset Not Valid"
    return Response(data, status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsLoggedOut])
def user_logout(request):
    serializer = CustomerLogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    token = request.auth.__str__()
    email = request.user.email
    key = f'{email[:email.index("@")]}_token'
    cache.set(key, token, timeout=20)
    return Response(
        data={"message": "Logged Out Successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )


@swagger_auto_schema(method="post", request_body=MerchantSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsLoggedOut])
def user_merchant_create(request):

    if Merchant.objects.filter(customer=request.user).exists():
        return Response(
            {"message": "User Is Already A Merchant"},
            status.HTTP_400_BAD_REQUEST,
        )
    print(Merchant.objects.all())
    serializer = MerchantSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(customer=request.user)
        data = {
            "merchant": serializer.data,
            "message": "Merchant Account Successfully Created",
        }
        print("merchant created")
        return Response(data=data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def verify_email(request):
    token = request.data["token"]
    usr = authenticate_token(token)
    if usr:
        usr.verified_email = True
        usr.save()
        token = RefreshToken.for_user(usr)
        serializer = RetrieveCustomerSerializer(
            usr, context={"request": request}
        )
        data = {
            "data": serializer.data,
            "message": "Email Successfully Verified",
            "token": {
                "refresh": str(token),
                "access": str(token.access_token),
            },
        }
        return Response(data, status.HTTP_200_OK)


@api_view(["POST"])
def resend_email(request):
    token = request.data["token"]
    try:
        user = AuthToken.objects.get(key=token).user
    except AuthToken.DoesNotExist:
        return Response(
            {"message": "Invalid Token"}, status.HTTP_400_BAD_REQUEST
        )
    email = send_verify_email(user, request)

    return Response(
        {"message": "Verification Email Resent"}, status.HTTP_200_OK
    )
