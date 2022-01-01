from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer, Merchant

User = get_user_model()


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"
        read_only_fields = ["customer"]


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    # photo = serializers.SerializerMethodField()
    # merchant = MerchantSerializer()

    class Meta:
        model = Customer
        exclude = ["password"]
        depth = 1

    """this section not needed right now because of cloudinary"""
    # def photo_url(self, obj):
    #     try:
    #         url = obj.photo.url
    #     except ValueError:
    #         url = "/media/default/default.jpg"
    #     return url

    # def get_photo(self, obj):

    #     request = self.context["request"]
    #     image_url = self.photo_url(obj)
    #     url = request.build_absolute_uri(location=image_url)
    #     return url


class UpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "photo",
            "phone_number",
            "first_name",
            "last_name",
            "university",
        ]
        read_only_fields = [
            "id",
            "email",
            "is_active",
            "status",
            "last_login",
            "created",
            "is_staff",
            "agreed_to_terms",
            "verified_email",
        ]


class CreateCustomerSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    university = serializers.CharField(required=True)
    agreed_to_terms = serializers.BooleanField(required=True)

    def validate(self, attrs):

        if attrs["password"] == attrs["password2"]:
            return super().validate(attrs)

        raise serializers.ValidationError(
            {"message": "Passwords Do Not Match"}, status.HTTP_400_BAD_REQUEST
        )

    def create(self, validated_data):
        password2 = validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        user.set_password(password2)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        print(self.user)
        if not self.user.verified_email:
            raise serializers.ValidationError(
                {"message": "Email Not Verified"}, status.HTTP_401_UNAUTHORIZED
            )
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user.last_login = timezone.now()
        user.save()
        token["first_name"] = user.first_name
        try:
            token["merchant_id"] = user.merchant.id
        except:
            token["merchant_id"] = None
        token["photo"] = user.photo.url
        return token


class CustomerPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_old_password(self, data):

        if not self.instance.check_password(data):
            raise serializers.ValidationError(
                {"message": "Old Password Is Invalid"}, status.HTTP_400_BAD_REQUEST
            )
        return data

    def validate(self, data):

        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"message": "Passwords Do Not Match"}, status.HTTP_400_BAD_REQUEST
            )
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password2"])
        instance.save()
        return instance


class CustomerUserPasswordResetConfirmSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"passwords": "Passwords Do Not Match"}, status.HTTP_400_BAD_REQUEST
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password2"])
        instance.save()
        return instance


class CustomerLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        self.refresh_token = attrs["refresh"]

        return attrs

    def save(self, **kwargs):
        try:

            RefreshToken(self.refresh_token).blacklist()

        except TokenError:
            serializers.ValidationError(
                {"message": "Not Logged Out"}, status.HTTP_400_BAD_REQUEST
            )
