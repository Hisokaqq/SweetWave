from signal import signal
from venv import create
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != "":
        user.username = user.email

pre_save.connect(updateUser,sender=User)

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user
        )

def deleteUser(sender, instance, **kwargs):
    user = instance.user

    user.delete()

post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)