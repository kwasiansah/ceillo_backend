from customer.models import Merchant
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from product.models import Category
User = get_user_model()


@pytest.fixture()
def login_details(client, db):
    endpoint = reverse('login')
    data = {'email': 'thomas@gmail.com', 'password': 'password'}
    response = client.post(path=endpoint, data=data)
    print(response.data)
    print(User.objects.all())
    yield response.data['access'], response.data['refresh']


def test_post_product_permission_denied(client, db, login_details):
    endpoint = reverse('post-product')
    data = {'name': 'socks', 'brand': 'apple', 'price': 217, 'description': 'black black black sheep have you any wool',
            'long_description': 'i have a little poney his name is dapple gray', 'in_stock': 20, 'active': True, 'rating': 10}
    response = client.post(path=endpoint, data=data, HTTP_AUTHORIZATION='Bearer ' +
                           login_details[0], content_type='application/json')
    print(response.data)
    assert response.data['detail'].__str__(
    ) == 'You do not have permission to perform this action.'


def test_post_product(client, db, login_details):
    endpoint = reverse('post-product')
    merchant = {'brand': 'mistubishi'}
    user = User.objects.get(email='thomas@gmail.com')
    merchant = Merchant.objects.create(**merchant, customer=user)
    data = {'name': 'socks', 'brand': 'apple', 'price': 217, 'description': 'black black black sheep have you any wool',
            'long_description': 'i have a little poney his name is dapple gray', 'in_stock': 20, 'active': True, 'rating': 10, 'category': 'toys'}
    category = Category.objects.create(
        name='toys', description='description', active=True)

    response = client.post(path=endpoint, data=data, HTTP_AUTHORIZATION='Bearer ' +
                           login_details[0], content_type='application/json')
    print(response.data)


# def test_post_product_get_method(client, db, login_details):
#     endpoint = reverse('post-product')
#     merchant = {'brand': 'mistubishi'}
#     user = User.objects.get(email='thomas@gmail.com')
#     merchant = Merchant.objects.create(**merchant, customer=user)
#     category = Category.objects.create(
#         name='toys', description='description', active=True)

#     response = client.get(path=endpoint, HTTP_AUTHORIZATION='Bearer ' +
#                           login_details[0], content_type='application/json')
#     print(response.data)
