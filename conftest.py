import pytest
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from customer.models import Merchant
from product.models import Category, Product

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        data = {
            "email": "thomas@gmail.com",
            "password": "password",
            "first_name": "test",
            "last_name": "unit",
            "university": "KNUST",
            "phone_number": "0200758003",
            "agreed_to_terms": True,
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
            "status": "ACTIVE",
            "verified_email": True,
        }
        user_a = User.objects.create_user(**data)


@pytest.fixture()
def login_details(client, db):
    login = reverse("login")
    data = {"email": "thomas@gmail.com", "password": "password"}
    response = client.post(path=login, data=data)
    return [response.data["access"], response.data["refresh"]]


@pytest.fixture()
def post_product(client, login_details, django_db_blocker):
    with django_db_blocker.unblock():
        endpoint = reverse("post-product")
        merchant = {"brand": "mistubishi"}
        user = User.objects.get(email="thomas@gmail.com")
        merchant = Merchant.objects.create(**merchant, customer=user)
        data = {
            "name": "socks",
            "brand": "apple",
            "price": 217,
            "description": "black black black sheep have you any wool",
            "long_description": "i have a little poney his name is dapple gray",
            "stock": 20,
            "active": True,
            "rating": 10,
            "category": 1,
        }
        category = Category.objects.create(
            name="toys", description="description", active=True
        )

        response = client.post(
            path=endpoint,
            data=data,
            HTTP_AUTHORIZATION="Bearer " + login_details[0],
            content_type="application/json",
        )
    print(response.data)


@pytest.fixture()
def product(django_db_blocker, post_product, db):
    product = Product.objects.get(name="socks")
    url = product.url_slug
    print(url)
    return url
