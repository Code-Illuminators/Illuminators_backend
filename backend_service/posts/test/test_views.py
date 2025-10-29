import pytest
import logging
import tempfile
from PIL import Image
from users.models import User
logger = logging.getLogger(__name__)
POST_TYPES = ["bigfoot", "ufo", "ghosts", "others"]
POST_MAP = {
    "bigfoot": "bigfoot_post",
    "ufo": "ufo_post",
    "ghosts": "ghost_post",
    "others": "other_post",
}
@pytest.mark.django_db
@pytest.mark.parametrize("post_type", POST_TYPES)
def test_add_post(api_client, user, post_type):
    """Test add post endpoint."""
    api_client.force_authenticate(user=user)
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    file.seek(0)

    with open(file.name, "rb") as image_file:
        response_create = api_client.post(
            f'/api/posts/{post_type}/create/',
            data={
                "location": "Forest near Kyiv",
                "image": image_file,
            },
            format="multipart"
        )
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 201 

@pytest.mark.django_db
@pytest.mark.parametrize("post_type,post_fixture", [
    ("bigfoot", "bigfoot_post"),
    ("ufo", "ufo_post"),
    ("ghosts", "ghost_post"),
    ("others", "other_post"),
])
def test_get_posts_list(api_client, user, request, post_type, post_fixture):
    """Test get posts endpoint."""
    post = request.getfixturevalue(post_fixture)
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/posts/{post_type}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
@pytest.mark.parametrize("post_type,post_fixture", [
    ("bigfoot", "bigfoot_post"),
    ("ufo", "ufo_post"),
    ("ghosts", "ghost_post"),
    ("others", "other_post"),
])
def test_get_user_posts(api_client, user, request, post_type, post_fixture):
    """Test get user posts endpoint."""
    post = request.getfixturevalue(post_fixture)
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/posts/{post_type}/user/{user.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
@pytest.mark.parametrize("post_type,post_fixture", [
    ("bigfoot", "bigfoot_post"),
    ("ufo", "ufo_post"),
    ("ghosts", "ghost_post"),
    ("others", "other_post"),
])
def test_update_post(api_client, user, request, post_type, post_fixture):
    """Test update bigfoot post endpoint."""
    post = request.getfixturevalue(post_fixture)
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f'/api/posts/{post_type}/{post.id}/update/',
        data={"location": "Updated Forest near Kyiv"},
        format="json"
    )
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
@pytest.mark.parametrize("post_type,post_fixture", [
    ("bigfoot", "bigfoot_post"),
    ("ufo", "ufo_post"),
    ("ghosts", "ghost_post"),
    ("others", "other_post"),
])
def test_delete_post(api_client, user, request, post_type, post_fixture):
    """Test delete post endpoint."""
    post = request.getfixturevalue(post_fixture)
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/posts/{post_type}/{post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 204

@pytest.mark.django_db
@pytest.mark.parametrize("post_type", POST_TYPES)
def test_get_posts_not_existing_user(api_client, user, post_type):
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/posts/{post_type}/user/9999/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
@pytest.mark.parametrize("post_type", POST_TYPES)
def test_get_posts_no_posts(api_client, post_type):
    """Test get user posts endpoint when user has no posts."""
    testuser=User.objects.create_user(username="nopostuser", password="nopostpass", email="one@gmail.com")
    api_client.force_authenticate(user=testuser)
    response = api_client.get(f'/api/posts/{post_type}/user/{testuser.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
@pytest.mark.parametrize("post_type", POST_TYPES)
def test_create_post_wrong_method(api_client, user, post_type):
    api_client.force_authenticate(user=user)
    response = api_client.post(f'/api/posts/{post_type}/create/')
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
@pytest.mark.parametrize("post_type", POST_TYPES)
def test_not_existing_post_update(api_client, user, post_type):
    api_client.force_authenticate(user=user)
    response = api_client.patch(f'/api/posts/{post_type}/9999/update/', data={
        "location": "Krakiw"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
@pytest.mark.parametrize("post_type", POST_TYPES)
def test_not_existing_post_delete(api_client, user, post_type):
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/posts/{post_type}/9999/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
@pytest.mark.parametrize("post_type,post_fixture", [
    ("bigfoot", "bigfoot_post"),
    ("ufo", "ufo_post"),
    ("ghosts", "ghost_post"),
    ("others", "other_post"),
])
def test_update_post_wronng_data(api_client, user, request, post_type, post_fixture):
    """Test update bigfoot post endpoint."""
    post = request.getfixturevalue(post_fixture)
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f'/api/posts/{post_type}/{post.id}/update/',
        data={"location": ""},
        format="json"
    )
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
@pytest.mark.parametrize("post_type,post_fixture", [
    ("bigfoot", "bigfoot_post"),
    ("ufo", "ufo_post"),
    ("ghosts", "ghost_post"),
    ("others", "other_post"),
])
def test_update_post__not_owner(api_client, user, request, post_type, post_fixture):
    """Test try to update post endpoint by not owner."""
    post = request.getfixturevalue(post_fixture)
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.patch(
        f'/api/posts/{post_type}/{post.id}/update/',
        data={"location": "Updated Forest near Kyiv"},
        format="json"
    )
    logger.info(f"{response.data}")
    assert response.status_code == 403

@pytest.mark.django_db
@pytest.mark.parametrize("post_type,post_fixture", [
    ("bigfoot", "bigfoot_post"),
    ("ufo", "ufo_post"),
    ("ghosts", "ghost_post"),
    ("others", "other_post"),
])
def test_delete_post__not_owner(api_client, user, request, post_type, post_fixture):
    """Test try to delete post endpoint by not owner."""
    post = request.getfixturevalue(post_fixture)
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.delete(f'/api/posts/{post_type}/{post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 403
