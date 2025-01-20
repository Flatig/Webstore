from django.contrib.auth.models import User
from django.db import models


def profile_image_upload(instance, filename):
    return 'profile_image/{0}/{1}'.format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=profile_image_upload, blank=True, default='static/images/no_image.jpg')
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_image(self):  # Use in template 'profile'
        return self.image.url if self.image and self.image.storage.exists(
            self.image.name) else '/static/images/no_image.jpg'
