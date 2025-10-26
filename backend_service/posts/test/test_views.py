import pytest
import logging
import tempfile
from PIL import Image
from users.models import User
logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_add_bifgoot(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    file.seek(0)

    with open(file.name, "rb") as image_file:
        response_create = api_client.post(
            '/api/posts/bigfoot/create/',
            data={
                "location": "Forest near Kyiv",
                "image": image_file,
            },
            format="multipart"
        )
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 201 

@pytest.mark.django_db
def test_add_ufo(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    image = Image.new('RGBA', size=(50, 50), color=(0, 155, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    file.seek(0)

    with open(file.name, "rb") as image_file:
        response_create = api_client.post(
            '/api/posts/ufo/create/',
            data={
                "location": "Sky above Lviv",
                "image": image_file,
            },
            format="multipart"
        )
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 201

@pytest.mark.django_db
def test_add_ghost(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    image = Image.new('RGBA', size=(50, 50), color=(0, 0, 155))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    file.seek(0)

    with open(file.name, "rb") as image_file:
        response_create = api_client.post(
            '/api/posts/ghosts/create/',
            data={
                "location": "Old house in Odessa",
                "image": image_file,
            },
            format="multipart"
        )
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 201

@pytest.mark.django_db
def test_add_other(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    image = Image.new('RGBA', size=(50, 50), color=(155, 155, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    file.seek(0)

    with open(file.name, "rb") as image_file:
        response_create = api_client.post(
            '/api/posts/others/create/',
            data={
                "location": "Mysterious place in Kharkiv",
                "image": image_file,
            },
            format="multipart"
        )
    logger.info(f"{response_create.data}")
    assert response_create.status_code == 201

@pytest.mark.django_db
def test_get_bigfoot_posts(api_client, bigfoot_post, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/posts/bigfoot/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_ufo_posts(api_client, ufo_post, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/posts/ufo/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_ghost_posts(api_client, ghost_post, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/posts/ghosts/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_other_posts(api_client, other_post, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/posts/others/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_user_bigfoot_posts(api_client, user, bigfoot_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/posts/bigfoot/user/{user.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_user_ufo_posts(api_client, user, ufo_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/posts/ufo/user/{user.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_user_ghost_posts(api_client, user, ghost_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/posts/ghosts/user/{user.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_user_other_posts(api_client, user, other_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/posts/others/user/{user.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_bigfoot_post(api_client, user, bigfoot_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch(f'/api/posts/bigfoot/{bigfoot_post.id}/update/', data={
        "location": "Updated Forest near Kyiv"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_bigfoot_post(api_client, user, bigfoot_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/posts/bigfoot/{bigfoot_post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 204

@pytest.mark.django_db
def test_update_ufo_post(api_client, user, ufo_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch(f'/api/posts/ufo/{ufo_post.id}/update/', data={
        "location": "Updated Sky above Lviv"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_ufo_post(api_client, user, ufo_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/posts/ufo/{ufo_post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 204

@pytest.mark.django_db
def test_update_ghost_post(api_client, user, ghost_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch(f'/api/posts/ghosts/{ghost_post.id}/update/', data={
        "location": "Updated Old house in Odessa"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_ghost_post(api_client, user, ghost_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/posts/ghosts/{ghost_post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 204

@pytest.mark.django_db
def test_update_other_post(api_client, user, other_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch(f'/api/posts/others/{other_post.id}/update/', data={
        "location": "Updated Mysterious place in Kharkiv"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_other_post(api_client, user, other_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/posts/others/{other_post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 204

@pytest.mark.django_db
def test_get_bigfoot_post_for_notexisting_user(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/posts/bigfoot/user/9999/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_ufo_post_for_notexisting_user(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/posts/ufo/user/9999/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_ghost_post_for_notexisting_user(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/posts/ghosts/user/9999/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_others_post_for_notexisting_user(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/posts/others/user/9999/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_user_with_no_posts_bigfoot(api_client) -> None:
    testuser=User.objects.create_user(username="nopostuser", password="nopostpass", email="one@gmail.com")
    api_client.force_authenticate(user=testuser)
    response = api_client.get(f'/api/posts/bigfoot/user/{testuser.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
def test_get_user_with_no_posts_ufo(api_client) -> None:
    testuser=User.objects.create_user(username="nopostuser", password="nopostpass", email="one@gmail.com")
    api_client.force_authenticate(user=testuser)
    response = api_client.get(f'/api/posts/ufo/user/{testuser.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
def test_get_user_with_no_posts_ghost(api_client) -> None:
    testuser=User.objects.create_user(username="nopostuser", password="nopostpass", email="one@gmail.com")
    api_client.force_authenticate(user=testuser)
    response = api_client.get(f'/api/posts/ghosts/user/{testuser.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
def test_get_user_with_no_posts_other(api_client) -> None:
    testuser=User.objects.create_user(username="nopostuser", password="nopostpass", email="one@gmail.com")
    api_client.force_authenticate(user=testuser)
    response = api_client.get(f'/api/posts/others/user/{testuser.id}/')
    logger.info(f"{response.data}")
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
def test_wrong_method_on_create_bigfoot(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/posts/bigfoot/create/')
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
def test_wrong_method_on_create_ufo(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/posts/ufo/create/')
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
def test_wrong_method_on_create_ghost(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/posts/ghosts/create/')
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
def test_wrong_method_on_create_other(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/posts/others/create/')
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
def test_not_existing_bigfoot_post_update(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch('/api/posts/bigfoot/9999/update/', data={
        "location": "Krakiw"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_not_existing_bigfoot_post_delete(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.delete('/api/posts/bigfoot/9999/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_not_existing_ufo_post_update(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch('/api/posts/ufo/9999/update/', data={
        "location": "Krakiw"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_not_existing_ufo_post_delete(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.delete('/api/posts/ufo/9999/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_not_existing_ghost_post_update(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch('/api/posts/ghosts/9999/update/', data={
        "location": "Krakiw"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_not_existing_ghost_post_delete(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.delete('/api/posts/ghosts/9999/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_not_existing_other_post_update(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch('/api/posts/others/9999/update/', data={
        "location": "Krakiw"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_not_existing_other_post_delete(api_client, user) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.delete('/api/posts/others/9999/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_update_bigfoot_wronng_data(api_client, user, bigfoot_post) -> None:
    api_client.force_authenticate(user=user)
    response = api_client.patch(f'/api/posts/bigfoot/{bigfoot_post.id}/update/', data={
        "location": ""
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 400

@pytest.mark.django_db
def test_try_update_bigfoot_post_not_owner(api_client, user, bigfoot_post) -> None:
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.patch(f'/api/posts/bigfoot/{bigfoot_post.id}/update/', data={
        "location": "Liubyni"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_try_delete_bigfoot_post_not_owner(api_client, user, bigfoot_post) -> None:
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.delete(f'/api/posts/bigfoot/{bigfoot_post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_try_update_ufo_post_not_owner(api_client, user, ufo_post) -> None:
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.patch(f'/api/posts/ufo/{ufo_post.id}/update/', data={
        "location": "Liubyni"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_try_delete_ufo_post_not_owner(api_client, user, ufo_post) -> None:
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.delete(f'/api/posts/ufo/{ufo_post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_try_update_ghost_post_not_owner(api_client, user, ghost_post) -> None:
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.patch(f'/api/posts/ghosts/{ghost_post.id}/update/', data={
        "location": "Liubyni"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_try_delete_ghost_post_not_owner(api_client, user, ghost_post) -> None:
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.delete(f'/api/posts/ghosts/{ghost_post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_try_update_other_post_not_owner(api_client, user, other_post) -> None:
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.patch(f'/api/posts/others/{other_post.id}/update/', data={
        "location": "Liubyni"
        }, format="json")
    logger.info(f"{response.data}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_try_delete_other_post_not_owner(api_client, user, other_post) -> None:
    other_user=User.objects.create_user(username="otheruser", password="otherpass", email="thief@gmail.com")
    api_client.force_authenticate(user=other_user)
    response = api_client.delete(f'/api/posts/others/{other_post.id}/delete/')
    logger.info(f"{response.data}")
    assert response.status_code == 403