import pytest

from django.contrib.auth import get_user_model
User = get_user_model()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        data = {'email': 'thomas@gmail.com', 'password': 'password', 'first_name': 'test', 'last_name': 'unit', 'address': 'Oyibi', 'phone_number': '0200758003',
                'date_of_birth': '29-12-2002', 'agreed_to_terms': True, 'is_active': True, 'is_staff': True, 'is_superuser': True, 'status': 'AC'}
        user_a = User.objects.create_user(**data)
