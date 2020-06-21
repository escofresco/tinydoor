import pytest
<<<<<<< HEAD
from django.test import RequestFactory
=======
>>>>>>> dd4fd56341cdf9156f4b0a7016225b2ebdc82048

from tinydoor.users.models import User
from tinydoor.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()
<<<<<<< HEAD


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
=======
>>>>>>> dd4fd56341cdf9156f4b0a7016225b2ebdc82048
