import pytest

@pytest.mark.django_db
def test_created_bigfootpost(bigfoot_post):
    """Test that a BigfootPost instance is created correctly."""
    assert bigfoot_post.location == "Lviv"
    assert bigfoot_post.image == "/photo_storage/photo_storage/ptah-3.jpg"

@pytest.mark.django_db
def test_created_ufopost(ufo_post):
    """Test that a UfoPost instance is created correctly."""
    assert ufo_post.location == "Kyiv"
    assert ufo_post.image == "/photo_storage/photo_storage/ptah-3_fRVkf9I.jpg"

@pytest.mark.django_db
def test_created_ghostpost(ghost_post):
    """Test that a GhostPost instance is created correctly."""
    assert ghost_post.location == "Odessa"
    assert ghost_post.image == "/photo_storage/photo_storage/ptah-5.jpg"

@pytest.mark.django_db
def test_created_otherpost(other_post):
    """Test that a OtherPost instance is created correctly."""
    assert other_post.location == "Kharkiv"
    assert other_post.image == "/photo_storage/photo_storage/ptah-6.jpg"

@pytest.mark.django_db
def test_post_owner(user, bigfoot_post, ufo_post, ghost_post, other_post):
    """Test that the owner of each post is set correctly."""
    assert bigfoot_post.owner == user
    assert ufo_post.owner == user
    assert ghost_post.owner == user
    assert other_post.owner == user

@pytest.mark.django_db
def test_post_str_methods(bigfoot_post, ufo_post, ghost_post, other_post):
    """Test the string representation of each post model."""
    assert str(bigfoot_post) == f"Bigfoot sighting by {bigfoot_post.owner.username} at {bigfoot_post.location}"
    assert str(ufo_post) == f"UFO sighting by {ufo_post.owner.username} at {ufo_post.location}"
    assert str(ghost_post) == f"Ghost encounter by {ghost_post.owner.username} at {ghost_post.location}"
    assert str(other_post) == f"Other report by {other_post.owner.username} at {other_post.location}"
