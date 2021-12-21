from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, Merchant
from rest_framework import status
from django.utils import timezone

User = get_user_model()


class MerchantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchant
        # fields = ['id', 'brand', 'id_card', 'id_card_type']
        fields = '__all__'


class CreateMerchantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchant
        fields = '__all__'
        read_only_fields = ['customer']


class ListCustomerSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(read_only=True, required=False)

    class Meta:
        model = Customer
        fields = '__all__'


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(read_only=True, required=False)

    class Meta:
        model = Customer
        fields = '__all__'


class UpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['photo', 'phone_number', 'first_name', 'last_name',
                  'date_of_birth', 'address', ]
        read_only_fields = ['id', 'email', 'is_active', 'status', 'last_login',
                            'created', 'is_staff', 'verified_email', 'agreed_to_terms']


# class CreateCustomerSerializer(TokenObtainPairSerializer):
#     password2 = serializers.CharField(write_only=True)
#     phone_number = serializers.CharField(required=True)
#     date_of_birth = serializers.CharField(required=True)
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)
#     address = serializers.CharField(required=True)
#     agreed_to_terms = serializers.BooleanField(required=True)

#     def validate_(self, attrs):

#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {'message': 'Passwords Do Not Match'}, status.HTTP_400_BAD_REQUEST)
#         return attrs

#     def validate(self, attrs):

#         try:
#             Customer.objects.get(email=attrs['email'])
#         except Customer.DoesNotExist:
#             del attrs['password2']
#             return attrs

#         raise serializers.ValidationError(
#             {"message": 'Email Already Exists'}, status.HTTP_400_BAD_REQUEST)

#     def create(self, validated_data):
#         user = Customer.objects.create_user(
#             **validated_data
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         # TODO: try authenticating users here but not important
#         refresh = self.get_token(user)
#         access = refresh.access_token
#         token = {'refresh': str(refresh), 'access': str(access)}
#         self.validated_data['token'] = token
#         return user

#     @classmethod
#     def get_token(cls, user):
#         token = RefreshToken.for_user(user)

#         token['first_name'] = user.first_name
#         return token

class CreateCustomerSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    agreed_to_terms = serializers.BooleanField(required=True)
    date_of_birth = serializers.CharField(required=True)

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist as e:
            return email

        raise serializers.ValidationError(
            {'message': 'Email Already Exists'}, status.HTTP_400_BAD_REQUEST)

    def validate(self, attrs):

        if attrs['password'] == attrs['password2']:
            return super().validate(attrs)

        raise serializers.ValidationError(
            {'message': 'Passwords Do Not Match'}, status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):

        password2 = validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(password2)
        user.save()

        token = RefreshToken.for_user(user)
        # TODO: this would be removed later
        token['first_name'] = user.first_name
        refresh = token
        access = token.access_token
        token = {'refresh': str(refresh), 'access': str(access)}

        self.validated_data['token'] = token
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # default_error_messages = {
    #     'message': _('not a valid email address')
    # }
    # # TODO: try and remove the errors from this serializer

    # def validate(self, attrs):
    #     try:
    #         data = super().validate(attrs)
    #     except exceptions.AuthenticationFailed:
    #         raise exceptions.AuthenticationFailed(
    #             self.default_error_messages, status.HTTP_400_BAD_REQUEST)
    #     return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user.last_login = timezone.now()
        user.save()
        token['first_name'] = user.first_name

        return token

# TODO: Serializer class not responding


class CustomerPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_old_password(self, data):

        if not self.instance.check_password(data):
            raise serializers.ValidationError(
                {"message": "Old Password Is Invalid"}, status.HTTP_400_BAD_REQUEST)
        return data

    def validate(self, data):

        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"message": "Passwords Do Not Match"}, status.HTTP_400_BAD_REQUEST)
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password2'])
        instance.save()
        return instance

    # SHA256: p2QAMXNIC1TJYWeIOttrVc98/R1BUFWu3/LiyKgUfQM


class CustomerUserPasswordResetConfirmSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {'passwords': 'Passwords Do Not Match'}, status.HTTP_400_BAD_REQUEST)
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password2'])
        instance.save()
        return instance


# data = {'email': 'mouse@gmail.com', 'password': 'prince', 'password2': 'princepk@123', 'first_name': 'mouse',
#         'last_name': 'ansah', 'address': 'accra', 'phone_number': '0200758003', 'date_of_birth': '29-12-2002', 'terms': True}
class CustomerLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        self.refresh_token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:

            RefreshToken(self.refresh_token).blacklist()

        except TokenError:
            serializers.ValidationError(
                {'message': 'Not Logged Out'}, status.HTTP_400_BAD_REQUEST)
