import pytest
from rest_framework.test import APIClient 
from users.models import User
from moderation.models import Vote, VoteLog

pytestmark = pytest.mark.django_db

@pytest.fixture
@pytest.mark.django_db
def user() -> User:
    """Create and return a test user."""
    return User.objects.create_user(username="testuser", password="qwerty", email="testemail@test.com", role="simple")

@pytest.fixture
@pytest.mark.django_db
def vote_create(user: User) -> Vote:
    """Create and return a test Vote."""
    vote = Vote.objects.create(
        nominated_user=user,
        vote_type="excommunication",
        roles_allowed_vote=["simple"],
    )
    VoteLog.objects.create(vote=vote, user=user)
    return vote

@pytest.fixture()  
def api_client() -> APIClient:  
    """  
    Fixture to provide an API client  
    """  
    yield APIClient()