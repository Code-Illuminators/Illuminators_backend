"""Module for defining Django models related to posts management"""
from django.db import models
from django.conf import settings

class BasePost(models.Model):
    """Class representing a base fields"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name="%(app_label)s_%(class)s_posts")
    location = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='./')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadata for BasePost"""
        abstract = True

class BigfootPost(BasePost):
    """Class representing a Bigfoot posts"""
    def __str__(self):
        """Return a string representation of the BigfootPost model"""
        return f"Bigfoot sighting by {self.owner.username} at {self.location}"

class UfoPost(BasePost):
    """Class representing a Ufo posts"""
    def __str__(self):
        """Return a string representation of the UfoPost model"""
        return f"UFO sighting by {self.owner.username} at {self.location}"

class GhostPost(BasePost):
    """Class representing a Ghost posts"""
    def __str__(self):
        """Return a string representation of the GhostPost model"""
        return f"Ghost encounter by {self.owner.username} at {self.location}"

class OtherPost(BasePost):
    """Class representing a Other posts"""
    def __str__(self):
        """Return a string representation of the OtherPost model"""
        return f"Other report by {self.owner.username} at {self.location}"
