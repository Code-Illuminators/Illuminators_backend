import pytest
from rest_framework.test import APIClient 
from users.models import User
from posts.models import BigfootPost, UfoPost, GhostPost, OtherPost

pytestmark = pytest.mark.django_db

@pytest.fixture
@pytest.mark.django_db
def user() -> User:
    """Create and return a test user."""
    return User.objects.create_user(username="testuser", password="qwerty", email="testemail@test.com", role="simple")

@pytest.fixture
@pytest.mark.django_db
def bigfoot_post(user: User) -> BigfootPost:
    """Create and return a test BigfootPost."""
    return BigfootPost.objects.create(
        owner=user,
        location="Lviv",
        created_at="2023-10-10T10:00:00Z",
        image="/photo_storage/photo_storage/ptah-3.jpg"
    )

@pytest.fixture
@pytest.mark.django_db
def ufo_post(user: User) -> UfoPost:
    """Create and return a test UfoPost."""
    return UfoPost.objects.create(
        owner=user,
        location="Kyiv",
        created_at="2023-11-11T11:00:00Z",
        image="/photo_storage/photo_storage/ptah-3_fRVkf9I.jpg"
    )

@pytest.fixture
@pytest.mark.django_db
def ghost_post(user: User) -> GhostPost:
    """Create and return a test GhostPost."""
    return GhostPost.objects.create(
        owner=user,
        location="Odessa",
        created_at="2023-12-12T12:00:00Z",
        image="/photo_storage/photo_storage/ptah-5.jpg"
    )

@pytest.fixture
@pytest.mark.django_db
def other_post(user: User) -> OtherPost:
    """Create and return a test OtherPost."""
    return OtherPost.objects.create(
        owner=user,
        location="Kharkiv",
        created_at="2024-01-01T13:00:00Z",
        image="/photo_storage/photo_storage/ptah-6.jpg"
    )

@pytest.fixture()  
def api_client() -> APIClient:  
    """  
    Fixture to provide an API client  
    """  
    yield APIClient()