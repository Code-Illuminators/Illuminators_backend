import pytest
import hashlib
from rest_framework.test import APIClient 
from users.models import Government, EntryPassword, User

pytestmark = pytest.mark.django_db


@pytest.fixture
@pytest.mark.django_db
def user() -> User:
    """Create and return a test user."""
    return User.objects.create_user(username="testuser", password="qwerty", email="testemail@test.com", role="simple")

@pytest.fixture
@pytest.mark.django_db
def entry_password() -> EntryPassword:
    """Create and return a test EntryPassword object with a hashed password."""
    entry_password = EntryPassword.objects.create(
        password_hash=hashlib.sha256("ert35hnbvcx".encode()).hexdigest()
    )
    return entry_password

@pytest.fixture
@pytest.mark.django_db
def government(user: User) -> Government:
    """Create and return a test Government object with a hashed IP address."""
    government = Government.objects.create(added_by=user)
    government.set_ip("172.32.23.10")
    government.save()
    return government

@pytest.fixture()  
def api_client() -> APIClient:  
    """  
    Fixture to provide an API client  
    """  
    yield APIClient()