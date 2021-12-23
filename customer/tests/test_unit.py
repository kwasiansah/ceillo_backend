import json
import os

import pytest
import pytest_django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from rest_framework import serializers

from customer.models import Merchant

User = get_user_model()
################################################################
################
# MODELS
################
################################################################


@pytest.fixture(scope="session")
def user_detail():
    data = {
        "email": "testing@gmail.com",
        "password": "password",
        "first_name": "test",
        "last_name": "unit",
        "university": "KNUST",
        "phone_number": "0200758003",
        "agreed_to_terms": True,
        "is_active": True,
        "is_staff": True,
        "is_superuser": True,
        "status": "AC",
    }
    return data


@pytest.fixture()
def create_user(user_detail, db):
    # first_name = 'test'
    # last_name = 'unit'
    # email = 'testing@gmail.com'
    # phone_number = '0200843453'
    # agreed_to_terms = True
    # university = 'KNUST'
    # password = 'password'
    # user_a = User.objects.create_user(first_name=first_name, password=password, last_name=last_name, email=email, phone_number=phone_number,
    #                                   agreed_to_terms=agreed_to_terms, university=university, date_of_birth=date_of_birth)
    # user_a.is_active = True
    # user_a.is_staff = True
    # user_a.is_superuser = True
    # user_a.status = 'AC'
    # user_a.set_password('password')
    # user_a.save()
    user_a = User.objects.create_user(**user_detail)
    return user_a


def test_fixture_inheritance_checks(create_user):
    user = create_user
    assert user.email == "testing@gmail.com"


################################################################
###################
# LOGIN
###################
################################################################


def test_login(create_user, client):

    login = reverse("login")
    data = {"email": "testing@gmail.com", "password": "password"}
    response = client.post(path=login, data=data)
    print(response.data)
    assert response


@pytest.fixture()
def login_details(client, create_user):
    login = reverse("login")
    data = {"email": "testing@gmail.com", "password": "password"}
    response = client.post(path=login, data=data)
    return [response.data["access"], response.data["refresh"]]


################################################################
#################
# DETAILS
#################
################################################################


def test_detail(login_details, client):
    detail = reverse("user_detail")
    response = client.get(path=detail, HTTP_AUTHORIZATION="Bearer " + login_details[0])
    user = response.renderer_context["request"].user
    print(response.data)
    assert response.data["data"]["email"] == user.email


################################################################
#################
# UPDATE
#################
################################################################


def test_put(login_details, client):
    update = reverse("user_update")
    data = {"first_name": "kwame"}
    response = client.put(
        path=update,
        data=data,
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
        fromat=json,
        content_type="application/json",
    )

    print(response.data)
    assert "kwame" in str(response.data)


def test_patch(login_details, client):
    update = reverse("user_update")
    data = {"first_name": "kwame"}
    response = client.patch(
        path=update,
        data=data,
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
        fromat=json,
        content_type="application/json",
    )
    print(response.data)
    assert "kwame" in str(response.data)


################################################################
#################
# PASSWORD CHANGE
#################
################################################################
def test_password_change(login_details, client):
    change = reverse("password-change")
    data = {
        "old_password": "password",
        "password": "testpassword",
        "password2": "testpassword",
    }
    response = client.post(
        path=change,
        data=data,
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
        content_type="application/json",
    )
    # TODO: validation error message not working
    user = User.objects.all()[0]
    print(user)
    print()
    print(response.data)
    assert user.check_password("password")
    assert response.renderer_context["request"].user.check_password("testpassword")
    assert response.status_code == 200


################################################################
##############
# SIGNUP PAGE
##############
################################################################


def test_create_field_required(db, client):
    data = {
        "emai": "mouse@gmail.com",
        "password": "prince",
        "password2": "princepk@123",
        "first_name": "mouse",
        "last_name": "ansah",
        "university": "KNUST",
        "phone_number": "0200758003",
        "terms": True,
    }
    create = reverse("user_create")
    response = client.post(path=create, data=data)
    print(response.data)
    assert response.data["email"][0].code == "required"


def test_create_password_do_match(db, client):
    data = {
        "email": "mouse@gmail.com",
        "password": "prince",
        "password2": "princepk@123",
        "first_name": "mouse",
        "last_name": "ansah",
        "university": "KNUST",
        "phone_number": "0200758003",
        "terms": True,
    }
    create = reverse("user_create")
    response = client.post(path=create, data=data)

    print(response.data)
    assert str(response.data["message"][0]) == "Passwords Do Not Match"


# if you need to review the name tuple go to python collections.__init__.OrderedDict


def test_create_email_already_exits(create_user, client):
    data = {
        "email": "testing@gmail.com",
        "password": "prince",
        "password2": "princepk@123",
        "first_name": "mouse",
        "last_name": "ansah",
        "university": "KNUST",
        "phone_number": "0200758003",
        "terms": True,
    }
    create = reverse("user_create")
    response = client.post(path=create, data=data)
    print(response.data)
    assert str(response.data["email"]["message"]) == "Email Already Exists"
    assert response.data["email"]["message"].code == 400


def test_create_successfull(db, client):
    data = {
        "email": "mouse@gmail.com",
        "password": "princepk@123",
        "password2": "princepk@123",
        "first_name": "mouse",
        "last_name": "ansah",
        "university": "KNUST",
        "phone_number": "0200758003",
        "agreed_to_terms": True,
    }
    create = reverse("user_create")
    response = client.post(path=create, data=data)
    print(response.data)
    assert "token" in response.data.keys()
    assert response.status_code == 201


# Todo i have to come back to this later
# TODO: use a regex for email validity in manager


def test_create_unseccessfull(db, client):
    data = {
        "email": "t",
        "password": "princepk@123",
        "password2": "princepk@123",
        "first_name": "mouse",
        "last_name": "ansah",
        "university": "KNUST",
        "phone_number": "0200758003",
        "agreed_to_terms": True,
    }
    create = reverse("user_create")
    response = client.post(path=create, data=data)
    print(response.data)


################################################################
##############
# LIST
##############
################################################################


def test_user_list(db, client, login_details):
    endpoint = reverse("user_list")
    response = client.get(
        path=endpoint,
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
        content_type="application/json",
    )
    print(response.data)
    assert "id" in response.data["data"][0] and "email" in response.data["data"][0]
    assert response.status_code == 200


################################################################
##############
# MERCHANT
##############
################################################################


@pytest.fixture()
def merchant_data():
    data = {"brand": "mistubishi"}
    return data


# TODO: this fixture is redundant would be changed later


# @pytest.fixture()
# def login_detail(client, db):
#     login = reverse('login')
#     data = {'email': 'thomas@gmail.com', 'password': 'password'}
#     response = client.post(path=login, data=data)
#     yield [response.data['access'], response.data['refresh']]


def test_merchant_create(client, login_details, merchant_data, db):
    endpoint = reverse("user-merchant-create")
    response = client.post(
        path=endpoint,
        data=merchant_data,
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
        content_type="application/json",
    )
    print(response.data)
    assert response.data["message"] == "Merchant Account Successfully Created"
    assert response.status_code == 201


def test_user_already_merchant(login_details, merchant_data, client, db):

    endpoint = reverse("user-merchant-create")
    response = client.post(
        path=endpoint,
        data=merchant_data,
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
        content_type="application/json",
    )
    request = response.renderer_context["request"]
    response = client.post(
        path=endpoint,
        data=merchant_data,
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
        content_type="application/json",
    )
    print(User.objects.all())
    print(response.data)


################################################################
##############
# REFRESH TOKEN
##############
################################################################


def test_refresh_token(client, login_details):
    endpoint = reverse("token-refresh")
    response = client.post(
        path=endpoint,
        data={"refresh": login_details[1]},
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
    )
    print(response.data)
    assert "access" in response.data
    assert response.status_code == 200


def test_invalid_refresh_token(client, login_details):
    endpoint = reverse("token-refresh")
    response = client.post(
        path=endpoint,
        data={"refresh": ""},
        HTTP_AUTHORIZATION="Bearer " + login_details[0],
    )

    print(response.data)
    assert response.data["refresh"][0].__str__() == "This field may not be blank."
    assert response.status_code == 400


################################################################
##############
# PASSWORD RESET
##############
################################################################


def test_password_reset():
    pass


################################################################
##############
# PASSWORD RESET CONFIRM
##############
################################################################


def test_password_reset_confirm():
    pass


################################################################
##############
# DELETE
##############
################################################################


def test_user_delete(client, login_details):
    endpoint = reverse("user_delete")
    response = client.delete(
        path=endpoint, HTTP_AUTHORIZATION="Bearer " + login_details[0]
    )
    print(response.data)
    assert response.data["message"] == "Account Deleted"


def test_verify_email(client, db):
    BASE_DIR = settings.BASE_DIR
    settings.EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

    settings.EMAIL_FILE_PATH = os.path.join(BASE_DIR.parent, "email")
    data = {
        "email": "mouse@gmail.com",
        "password": "princepk@123",
        "password2": "princepk@123",
        "first_name": "mouse",
        "last_name": "ansah",
        "university": "KNUST",
        "phone_number": "0200758003",
        "agreed_to_terms": True,
    }
    create = reverse("user_create")
    response = client.post(path=create, data=data)
    print(response.data)
    # verify_response = client.post
    assert "token" in response.data.keys()
    assert response.status_code == 201
