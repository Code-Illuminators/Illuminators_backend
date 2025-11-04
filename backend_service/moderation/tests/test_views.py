import pytest
import logging
from users.models import User

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_create_vote(api_client, user) -> None:
    """Test of creating a vote"""
    api_client.force_authenticate(user=user)
    testuser=User.objects.create_user(username="nopostuser", password="nopostpass", email="one@gmail.com")
    response_create = api_client.post('/api/moderation/votes/create/', data={
        "nominated_user": testuser.id, 
        "vote_type":"excommunication", 
        "roles_allowed_vote":["silver", "simple"],
        },  format="json")
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 202 

@pytest.mark.django_db
def test_create_vote_invalid_data(api_client, user) ->None:
    """Test of creating a vote with invalid data"""
    api_client.force_authenticate(user=user)
    testuser=User.objects.create_user(username="nopostuser", password="nopostpass", email="one@gmail.com")
    response_create = api_client.post('/api/moderation/votes/create/', data={
        "nominated_user": testuser.id, 
        "vote_type":"invalid", 
        "roles_allowed_vote":["silver", "simple"],
        },  format="json")
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 400

@pytest.mark.django_db
def test_votes_list(api_client, user, vote_create):
    """Test for obtaining active votes for user"""
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/moderation/votes/active/")
    logger.info(f"{response.data}")
    assert response.status_code == 200
    assert response.data[0]["nominated_user_username"] == user.username

@pytest.mark.django_db
def test_votes_list_unauthenticated(api_client):
    """Test for obtaining active votes for an unauthenticated user"""
    response = api_client.get("/api/moderation/votes/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_collect_vote_for_choice(api_client, user, vote_create):
    """Test of collecting voting results from user"""
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/moderation/votes/{vote_create.id}/vote/",
        {"choice": "for"},
        format="json",
    )
    logger.info(f"{response.data}")
    assert response.status_code == 202
    assert response.data["for_amount"] == 1
    assert response.data["against_amount"] == 0

@pytest.mark.django_db
def test_collect_vote_invalid(api_client, user, vote_create):
    """Test of collecting voting results from user with invalid data"""
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/moderation/votes/{vote_create.id}/vote/",
        {"choice": "invalid"},
        format="json",
    )
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
def test_collect_vote_invalid_pk(api_client, user, vote_create):
    """Test of collecting voting results for a non-existent vote"""
    api_client.force_authenticate(user=user)
    response = api_client.post("/api/moderation/votes/9999/vote/",
        {"choice": "for"},
        format="json",
    )
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_all(api_client, user):
    """Test of deletion of all data from the database"""
    golduser=User.objects.create_user(username="nopostuser", password="nopostpass", email="one@gmail.com", role="gold")
    api_client.force_authenticate(user=golduser)
    response = api_client.delete("/api/moderation/delete-all/")
    assert response.status_code == 200
    assert "success" in response.data

@pytest.mark.django_db
def test_delete_all_not_gold(api_client, user):
    """Test of deletion of all data from the database by a user without access rights"""
    api_client.force_authenticate(user=user)
    response = api_client.delete("/api/moderation/delete-all/")
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_user_account_success(api_client, user):
    """Test to delete a user"""
    response = api_client.delete(f"/api/moderation/votes/result/{user.username}/delete/")
    assert response.status_code == 200
    assert "success" in response.data
    assert not User.objects.filter(username=user.username).exists()

@pytest.mark.django_db
def test_delete_user_account_unexists(api_client, user):
    """Test to delete a user that does not exist"""
    response = api_client.delete("/api/moderation/votes/result/vasyl/delete/")
    assert response.status_code == 404
