import pytest
import logging
import json
logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_backup_posts(api_client, user, bigfoot_post, ufo_post, ghost_post, other_post):
    """Test that backup endpoint returns JSON with all post types"""
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/snapshot/backup/')
    assert response.status_code == 200
    assert response["Content-Type"] == "application/json"
    data = json.loads(response.content)
    assert "bigfoot" in data
    assert "ufo" in data
    assert "ghost" in data
    assert "other" in data
    assert len(data["bigfoot"]) == 1
    assert len(data["ufo"]) == 1
    assert len(data["ghost"]) == 1
    assert len(data["other"]) == 1

@pytest.mark.django_db
def test_restore_posts(api_client, user):
    """Test that restore endpoint correctly creates posts from JSON data"""
    api_client.force_authenticate(user=user)
    backup_data = {
        "bigfoot": [{
            "id": 5,
            "image": "ptah-6_9ICgTgy.jpg",
            "owner": "testuser",
            "location": "Kyiv",
            "lat": 1.23,
            "lng": 1.5768,
            "created_at": "2025-11-06T00:14:39.030304Z"
        }],
        "ufo": [],
        "ghost": [],
        "other": []
    }
    response = api_client.post('/api/snapshot/restore/', data=backup_data, format='json')
    assert response.status_code == 201
    assert response.data["count"] == 1
    assert response.data["status"] == "Restore successful"
