"""Configuring the handler for requests."""
from .models import BigfootPost, UfoPost, GhostPost, OtherPost
from .serializers import (
    BigfootPostSerializer, UfoPostSerializer,
    GhostPostSerializer, OtherPostSerializer
)
from .general_view import (
    get_all_posts,
    get_user_posts,
    create_post,
    update_post,
    delete_post
)

all_bigfoot = get_all_posts(BigfootPost, BigfootPostSerializer)
user_bigfoot = get_user_posts(BigfootPost, BigfootPostSerializer)
create_bigfoot = create_post(BigfootPostSerializer)
update_bigfoot = update_post(BigfootPost, BigfootPostSerializer)
delete_bigfoot = delete_post(BigfootPost)

all_ufo = get_all_posts(UfoPost, UfoPostSerializer)
user_ufo = get_user_posts(UfoPost, UfoPostSerializer)
create_ufo = create_post(UfoPostSerializer)
update_ufo = update_post(UfoPost, UfoPostSerializer)
delete_ufo = delete_post(UfoPost)

all_ghosts = get_all_posts(GhostPost, GhostPostSerializer)
user_ghosts = get_user_posts(GhostPost, GhostPostSerializer)
create_ghosts = create_post(GhostPostSerializer)
update_ghosts = update_post(GhostPost, GhostPostSerializer)
delete_ghosts = delete_post(GhostPost)

all_others = get_all_posts(OtherPost, OtherPostSerializer)
user_others = get_user_posts(OtherPost, OtherPostSerializer)
create_others = create_post(OtherPostSerializer)
update_others = update_post(OtherPost, OtherPostSerializer)
delete_others = delete_post(OtherPost)