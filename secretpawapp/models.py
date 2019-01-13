from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CharacterNSFWTypes(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, upload_to='avatar')
    facebook = models.URLField(max_length=250, unique=True)
    status = models.TextField(max_length=250, blank=True)
    is_verified = models.BooleanField(default=False)
    description = models.TextField(max_length=2000, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.user.username


class Character(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, upload_to='character')
    picture_author = models.CharField(max_length=50)
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
    nsfw = models.ManyToManyField(CharacterNSFWTypes, blank=True)
    description = models.TextField(max_length=250, blank=True)
    hints = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Gift(models.Model):
    giver = models.OneToOneField(Profile, related_name='giver', on_delete=models.DO_NOTHING)
    recipient = models.OneToOneField(Profile, related_name='recipient', on_delete=models.DO_NOTHING)
    picture = models.ImageField(upload_to='gift', null=True)
    wishes = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.giver.user.username + " > " + self.recipient.user.username


class Setting(models.Model):
    """
    Model for site-wide settings.
    """
    name = models.CharField(max_length=200, unique=True, help_text="Name of site-wide variable")
    value = models.CharField(max_length=250, null=True, blank=True, help_text="Value of site-wide variable that "
                                                                              "scripts can reference")

    def __str__(self):
        return self.name


@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.is_active = False

