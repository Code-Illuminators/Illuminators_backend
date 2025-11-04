import pytest
import math
from moderation.models import Vote, VoteLog
from users.models import User

@pytest.mark.django_db
def test_vote_creation(vote_create, user):
    """Test Vote instance is created correctly."""
    vote = vote_create
    assert vote.nominated_user == user
    assert vote.vote_type == "excommunication"
    assert vote.roles_allowed_vote == ["simple"]
    assert vote.for_amount == 0
    assert vote.against_amount == 0
    assert math.isclose(vote.progress, 0.0, rel_tol=1e-9)

    assert str(vote) == f"Vote for {user.username} — For: 0, Against: 0"

@pytest.mark.django_db
def test_votelog_creation(vote_create, user):
    """Test of creating a VoteLog for a user and vote."""
    vote = vote_create
    votelog = VoteLog.objects.create(vote=vote, user=user)
    assert votelog.vote == vote
    assert votelog.user == user
    assert votelog.is_for == False
    assert votelog.is_against == False
    assert votelog.status == False
    assert str(votelog) == f"VoteLog for {user.username} on vote {vote.id}"

@pytest.mark.django_db
def test_vote_update_progress(user):
    """Test the update_progress method in Vote"""
    vote = Vote.objects.create(
        nominated_user=user,
        vote_type="excommunication",
        roles_allowed_vote=["simple"],
    )
    user1 = User.objects.create_user(username="vasyl", password="123", role="simple")
    user2 = User.objects.create_user(username="john", password="123", role="simple")

    VoteLog.objects.create(vote=vote, user=user1, status=True, is_for=True)
    VoteLog.objects.create(vote=vote, user=user2, status=False)

    vote.update_progress()
    assert math.isclose(vote.progress, 50.0, rel_tol=1e-9)