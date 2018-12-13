from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class Profile(models.Model):
    firstname = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    image = models.CharField(max_length=255, default='')
    birthday = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=50, default='')
<<<<<<< HEAD
    bio = models.TextField(default='')
=======
    bio = models.TextField(default='my auto bio')
>>>>>>> ce71ac7... [FEATURE #161966915] setup userprofiles app
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=get_user_model())
