from django.db import models
from django.conf import settings

class BasePost(models.Model):
    """Class representing a base fields"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_posts")
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photo_storage/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class BigfootPost(BasePost):
    """Class representing a Bigfoot posts"""
    def __str__(self):
        return f"Bigfoot sighting by {self.owner.username} at {self.location}"

class UfoPost(BasePost):
    """Class representing a Ufo posts"""
    def __str__(self):
        return f"UFO sighting by {self.owner.username} at {self.location}"

class GhostPost(BasePost):
    """Class representing a Ghost posts"""
    def __str__(self):
        return f"Ghost encounter by {self.owner.username} at {self.location}"

class OtherPost(BasePost):
    """Class representing a Other posts"""
    def __str__(self):
        return f"Other report by {self.owner.username} at {self.location}"
