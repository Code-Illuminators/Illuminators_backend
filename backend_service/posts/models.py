from django.db import models
from django.conf import settings

class BasePost(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_posts")
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photo_storage/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class BigfootPost(BasePost):
    def __str__(self):
        return f"Bigfoot sighting by {self.owner.username} at {self.location}"

class UfoPost(BasePost):
    def __str__(self):
        return f"UFO sighting by {self.owner.username} at {self.location}"

class GhostPost(BasePost):
    def __str__(self):
        return f"Ghost encounter by {self.owner.username} at {self.location}"

class OtherPost(BasePost):
    def __str__(self):
        return f"Other report by {self.owner.username} at {self.location}"
