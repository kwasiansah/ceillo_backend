from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, Merchant
from rest_framework import status


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['name', 'id_char']


class ListCustomerSerializer(serializers.ModelSerializer):

    merchant = MerchantSerializer(read_only=True, required=False)

    class Meta:
        model = Customer
        fields = ["customer_id", 'photo', 'email', 'phone_number', 'first_name',
                  'last_name', 'password', 'date_of_birth', 'terms', 'merchant']


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(read_only=True, required=False)

    class Meta:
        model = Customer
        fields = ["customer_id", 'photo', 'email', 'phone_number', 'first_name', 'last_name', 'password',
                  'date_of_birth', 'address', 'terms', 'merchant', 'is_superuser', 'is_active', 'is_staff', 'status']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        """ NOTE this is for testing only the password change view would be created seperately """
        if validated_data.get('password', False):
            instance.set_password(validated_data['password'])
            instance.save()
        return instance

# class CreateCustomerSerializer(serializers.ModelSerializer):
#     # user = UserSerializer()
#     password2 = serializers.CharField(write_only=True)
#     # merchant = MerchantSerializer()

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {'password': 'password do not match'})
#         del attrs['password2']
#         return super().validate(attrs)

#     def create(self, validated_data):
#         # merchant = validated_data.pop['merchant']
#         # del validated_data['merchant']
#         """ password1 = validated_data['password']
#         password2 = validated_data['password2']
#         if password1 != password2:
#             raise serializers.ValidationError('passwords do not match')
#         del validated_data['password2'] """
#         # this validation is not used
#         try:
#             Customer.objects.get(email=validated_data['email'])
#         except Customer.DoesNotExist:
#             print('the email error occured')
#         else:
#             raise serializers.ValidationError({"email": 'email exist'})

#         groups = validated_data.pop('groups', [])
#         # print(groups)
#         user_perm = validated_data.pop('user_permissions', [])

#         # print(user_perm)

#         # del validated_data['groups']
#         # del validated_data['user_permissions']
#         user = Customer.objects.create_user(
#             **validated_data
#         )
#         user.set_password(validated_data['password'])
#         user.groups.set(groups)
#         user.user_permissions.set(user_perm)
#         user.save()

#         return user

#     class Meta:
#         model = Customer
#         # fields = ["customer_id", "",'photo', 'email', 'phone_number', 'first_name', 'last_name','password', 'terms', 'merchant']
#         fields = ['first_name', 'last_name', 'email', 'phone_number',
#         'date_of_birth', 'address', 'password', 'password2']


class CreateCustomerSerializer(TokenObtainPairSerializer):
    password2 = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=True)
    date_of_birth = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    terms = serializers.BooleanField(required=True)

    def validate_password_match(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'password do not match'}, status.HTTP_400_BAD_REQUEST)
        return attrs

    def validate(self, attrs):
        try:
            Customer.objects.get(email=attrs['email'])
        except Customer.DoesNotExist:
            del attrs['password2']
            return attrs

        raise serializers.ValidationError(
            {"email": 'email exist'}, status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):
        user = Customer.objects.create_user(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        # TODO: try authenticating users here but not important
        refresh = self.get_token(user)
        access = refresh.access_token
        token = {'refresh': str(refresh), 'access': str(access)}
        self.validated_data['token'] = token
        return user

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)

        token['first_name'] = user.first_name
        return token


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'message': _('not a valid email address')
    }
    # TODO: try and remove the errors from this serializer

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                self.default_error_messages, status.HTTP_400_BAD_REQUEST)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['first_name'] = user.first_name

        return token


class CustomerPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_old_password(self, data):
        if not self.instance.check_password(data):
            raise serializers.ValidationError(
                {"message": "old password is invalid"}, status.HTTP_400_BAD_REQUEST)
        return data

    def validate(self, data):
        data = super().validate(data)
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "passwords do not match"}, status.HTTP_400_BAD_REQUEST)
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
                {'passwords': 'passwords do not match'}, status.HTTP_400_BAD_REQUEST)
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password2'])
        instance.save()
        return instance
