import pytest
from django.core.exceptions import ValidationError
from users.models import User

@pytest.mark.django_db
def test_government_ip_hashing(government):
    """Test that the Government model correctly hashes and checks IP addresses."""
    ip_address = "172.32.23.10"
    assert government.check_ip(ip_address) is True

@pytest.mark.django_db
def test_entry_password_hashing(entry_password):
    """Test that the EntryPassword model correctly hashes and checks passwords."""
    raw_password = "ert35hnbvcx"
    assert entry_password.check_password(raw_password) is True

@pytest.mark.django_db
def test_user_creation(user):
    """Test that a User instance is created correctly."""
    assert user.username == "testuser"
    assert user.email == "testemail@test.com"
    assert user.role == "simple"
    assert user.check_password("qwerty") is True

@pytest.mark.django_db
def test_user_invalid_role():
    """Test that creating a User with an invalid role raises a ValidationError."""
    with pytest.raises(ValidationError):
        user = User(username="invaliduser", role="invalid_role")
        user.full_clean()

@pytest.mark.django_db
def test_government_ip_invalid(government):
    """Test that the Government model correctly identifies an invalid IP address."""
    invalid_ip = "192.2.23.10"
    assert government.check_ip(invalid_ip) is False

@pytest.mark.django_db
def test_entry_password_invalid(entry_password):
    """Test that the EntryPassword model correctly identifies an invalid password."""
    invalid_password = "lkjhbvgbhn"
    assert entry_password.check_password(invalid_password) is False


