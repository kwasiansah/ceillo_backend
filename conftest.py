import pytest
from django.contrib.auth import get_user_model

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
