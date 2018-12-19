from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True)
    facebook = models.URLField(max_length=250, unique=True)
    status = models.TextField(max_length=250, blank=True)
    is_verified = models.BooleanField(default=False)
    description = models.TextField(max_length=2000, blank=True)
    tags = models.ManyToManyField(Tag)


class CharacterNSFWTypes(models.Model):
    name = models.CharField(max_length=50)


class Character(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    picture = models.ImageField(null=True)
    picture_author = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    race = models.CharField(max_length=50, blank=True)
    SEX = (
        ('W', 'Girl'),
        ('M', 'Boy'),
        ('O', 'Other'),
    )
    sex = models.CharField(choices=SEX, max_length=1)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    nsfw = models.ManyToManyField(CharacterNSFWTypes)
    description = models.TextField(max_length=250, blank=True)
    hints = models.TextField(max_length=100, blank=True)


class Gift(models.Model):
    giver = models.ForeignKey(Profile, related_name='giver', on_delete=models.DO_NOTHING)
    recipient = models.ForeignKey(Profile, related_name='recipient', on_delete=models.DO_NOTHING)
    picture = models.ImageField()
    wishes = models.ImageField(null=True)


class Setting(models.Model):
    """
    Model for site-wide settings.
    """
    name = models.CharField(max_length=200, unique=True, help_text="Name of site-wide variable")
    value = models.CharField(max_length=250, null=True, blank=True, help_text="Value of site-wide variable that "
                                                                              "scripts can reference")


@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.is_active = False

