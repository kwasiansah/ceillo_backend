import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from customer.models import Customer
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, force_authenticate

User = get_user_model()

# Create your tests here.


class CustomerTestCase(TestCase):
    def setUp(self):
        first_name = "test"
        last_name = "unit"
        email = "testing@gmail.com"
        phone_number = "0200843453"
        agreed_to_terms = True
        university = "Oyibi"
        date_of_birth = "30-6-1943"
        user_a = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            agreed_to_terms=agreed_to_terms,
            university=university,
            date_of_birth=date_of_birth,
        )
        user_a.is_active = True
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.status = "AC"
        user_a.set_password("sometest@123")
        self.user_a_pw = "sometest@123"
        user_a.save()
        self.user_a = user_a

    def test_user_exits(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        self.assertTrue(self.user_a.check_password("sometest@123"))

    def test_user_admin(self):
        self.user_a.is_active = True
        self.assertTrue(
            self.user_a.is_active and self.user_a.is_staff and self.user_a.is_superuser
        )

    def test_user_active(self):
        self.assertTrue(self.user_a.status == "AC")

    def test_login_url(self):
        login_url = "/auth/login/"
        reverse_url = reverse("login")
        self.assertTrue(reverse_url == login_url)
        data = {"email": "testing@gmail.com", "password": "sometest@123"}
        # data = {'email': self.user_a.email, 'password': self.user_a.password}

        response = Client().post(login_url, data, format=json)
        self.refresh = response.data["refresh"]
        self.access = response.data["access"]
        response = self.client.get(
            reverse("user_detail"),
            HTTP_AUTHORIZATION="Bearer " + response.data["access"],
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticate_user(self):
        print(settings.AUTH_USER_MODEL)
        user = authenticate(email=self.user_a.email, password="sometest@123")
        self.assertTrue(user)

    # def test_detail_view(self):
    #     response = self.client.get(reverse('user_detail'), HTTP_AUTHORIZATION = self.access)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
