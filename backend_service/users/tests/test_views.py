import pytest
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_register_user(api_client) -> None:
    """Test user registration endpoint."""
    response_create = api_client.post('/api/auth/register/', data={
        "username": "username", 
        "email":"user@email.com", 
        "password":"password"
        },  format="json")
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 201 

@pytest.mark.django_db
def test_register_user_invalid_data(api_client) -> None:
    """Test user registration endpoint with invalid data."""
    response_create = api_client.post('/api/auth/register/', data={
        "username": "", 
        "email":"invalid_email", 
        "password":""
        },  format="json")
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 400

@pytest.mark.django_db
def test_login_user(api_client, user) -> None:
    """Test user login endpoint."""
    response = api_client.post('/api/auth/login/', data={
        "username": "testuser", 
        "password":"qwerty"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_user_invalid_credentials(api_client, user) -> None:
    """Test user login endpoint with invalid credentials."""
    response = api_client.post('/api/auth/login/', data={
        "username": "wronguser", 
        "password":"wrongpassword"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
def test_logout_user(api_client, user) -> None:
    """Test user logout endpoint."""
    login_response = api_client.post('/api/auth/login/', data={
        "username": "testuser",
        "password":"qwerty"
        }, format="json")
    refresh_token = login_response.data['refresh']
    response = api_client.post('/api/auth/logout/', data={
        "refresh": refresh_token
        }, format="json")  
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_change_password(api_client, user) -> None:
    """Test change password endpoint."""
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/auth/change-password/', data={
        "old_password": "qwerty",
        "new_password": "newpassword"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_users_list(api_client, user) -> None:
    """Test users list endpoint."""
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/auth/users/')
    logger.info(f"{response.data}")
    assert response.status_code == 200 

@pytest.mark.django_db
def test_users_list_unauthenticated(api_client) -> None:
    """Test users list endpoint without authentication."""
    response = api_client.get('/api/auth/users/')
    logger.info(f"{response.data}")
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_active_password(api_client, entry_password) -> None:
    """Test get active entry password endpoint."""
    headers = {"X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN}
    response = api_client.get('/api/auth/entry-password/active/', headers=headers)
    logger.info(f"{response.data}")
    assert response.status_code == 200
    assert response.data['exists'] is True

@pytest.mark.django_db
def test_get_active_password_no_password(api_client, user) -> None:
    """Test get active entry password endpoint when no password exists."""
    headers = {"X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN}
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/auth/entry-password/active/', headers=headers)
    logger.info(f"{response.data}")
    assert response.status_code == 400
    assert response.data['exists'] is False

@pytest.mark.django_db
def test_delete_entry_password(api_client, entry_password) -> None:
    """Test delete entry password endpoint."""
    headers = {"X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN}
    response = api_client.delete(f'/api/auth/entry-password/delete/{entry_password.id}/', headers=headers)
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_entry_password_not_found(api_client) -> None:
    """Test delete entry password endpoint when password not found."""
    headers = {"X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN}
    response = api_client.delete('/api/auth/entry-password/delete/9999/', headers=headers)
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_set_entry_password(api_client) -> None:
    """Test set entry password endpoint."""
    headers = {"X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN}
    response = api_client.post('/api/auth/entry-password/set/', headers=headers, data={
        "password": "new_entry_password"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 201

@pytest.mark.django_db
def test_check_entry_password(api_client, entry_password) -> None:
    """Test check entry password endpoint."""
    response = api_client.post('/api/auth/entry-password/check/', data={
        "password": "ert35hnbvcx"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 200
    assert response.data['valid'] is True

@pytest.mark.django_db
def test_check_entry_password_invalid(api_client, entry_password) -> None:
    """Test check entry password endpoint with invalid password."""  
    response = api_client.post('/api/auth/entry-password/check/', data={
        "password": "wrong_password"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 400
    assert response.data['valid'] is False

@pytest.mark.django_db
def test_report_government_ip(api_client, user) -> None:
    """Test report government IP endpoint."""
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/auth/report-hunter-ip/', data={
        "ip_address": "172.32.20.4",
        "added_by": user.id
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 201

@pytest.mark.django_db
def test_report_government_ip_unauthenticated(api_client) -> None:
    """Test report government IP endpoint without authentication."""
    response = api_client.post('/api/auth/report-hunter-ip/', data={
        "ip_address": "192.62.15.20"
        }, format="json")  
    logger.info(f"{response.data}")
    assert response.status_code == 401

@pytest.mark.django_db
def test_report_government_ip_invalid_data(api_client, user) -> None:
    """Test report government IP endpoint with invalid data."""
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/auth/report-hunter-ip/', data={
        "ip_address": "1742.32.20.400"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 400