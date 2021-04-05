from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(default='default.jpg', upload_to='profile_pictures')
    about = models.TextField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.user_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.user_image.path)