import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.client import Client
import pytest
from rest_framework import serializers
User = get_user_model()


@pytest.fixture()
def create_user(db):
    first_name = 'test'
    last_name = 'unit'
    email = 'testing@gmail.com'
    phone_number = '0200843453'
    agreed_to_terms = True
    address = 'Oyibi'
    date_of_birth = '30-6-1943'
    user_a = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                  agreed_to_terms=agreed_to_terms, address=address, date_of_birth=date_of_birth)
    user_a.is_active = True
    user_a.is_staff = True
    user_a.is_superuser = True
    user_a.status = 'AC'
    user_a.set_password('password')
    user_a.save()
    return user_a


def test_passing(create_user):
    user = create_user
    assert user.email == 'testing@gmail.com'


def test_login(create_user, client):
    login = reverse('login')
    data = {'email': 'testing@gmail.com', 'password': 'password'}
    response = client.post(path=login, data=data)
    print(response.data)
    assert response


@pytest.fixture()
def login_details(client, create_user):
    login = reverse('login')
    data = {'email': 'testing@gmail.com', 'password': 'password'}
    response = client.post(path=login, data=data)
    return [response.data['access'], response.data['refresh']]


def test_detail(login_details, client, create_user):
    detail = reverse('user_detail')
    response = client.get(
        path=detail, HTTP_AUTHORIZATION='Bearer ' + login_details[0])
    print(response.data)
    assert response.data['data']['email'] == create_user.email


def test_put(login_details, client):
    update = reverse('user_update')
    data = {"first_name": "kwame"}
    response = client.put(path=update, data=data,
                          HTTP_AUTHORIZATION='Bearer ' + login_details[0], fromat=json, content_type='application/json')
    print(response.data)
    assert 'kwame' in str(response.data)


def test_patch(login_details, client):
    update = reverse('user_update')
    data = {"first_name": "kwame"}
    response = client.patch(path=update, data=data,
                            HTTP_AUTHORIZATION='Bearer ' + login_details[0], fromat=json, content_type='application/json')
    print(response.data)
    assert 'kwame' in str(response.data)


def test_password_change(login_details, client):
    change = reverse('password-change')
    data = {'old_password': 'password',
            'password': 'testpassword', 'password2': 'testpassword', }
    response = client.post(path=change, data=data, HTTP_AUTHORIZATION='Bearer ' +
                           login_details[0], content_type='application/json')
    # TODO: validation error message not working
    user = User.objects.all()[0]
    print(user)
    print(response.status_code)
    assert user.check_password('testpassword')
