from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django_registration.forms import RegistrationFormUniqueEmail
from django import forms

from secretpaw import settings
from secretpawapp.models import Profile, Tag, Character, CharacterNSFWTypes


def validate_secret_correctness(secret):
    if not hash(secret) == hash(settings.PAWGATE_SECRET):
        raise forms.ValidationError('Wrong secret')


class PawgateForm(forms.Form):
    secret = forms.CharField()

    def clean_secret(self):
        secret = self.cleaned_data.get('secret')
        validate_secret_correctness(secret)

        return secret


def validate_unique_facebook(facebook):
    if Profile.objects.filter(facebook=facebook).exists():
        raise forms.ValidationError('This facebook profile link is already in use')


validate_is_a_facebook_link = RegexValidator('facebook\.com', 'Enter a valid facebook profile url')


class RegistrationFormUniqueEmailAndFacebook(RegistrationFormUniqueEmail):
    facebook = forms.URLField(
        error_messages={
            'required': 'You must give your facebook profile link',
        }
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()

            user.profile = Profile.objects.create(user=user, facebook=self.cleaned_data['facebook'])
            user.profile.save()
        return user

    def clean_facebook(self):
        facebook = self.cleaned_data.get('facebook')
        validate_is_a_facebook_link(facebook)
        validate_unique_facebook(facebook)

        return facebook


def validate_max_size(image):
    if image.size > 5*1024*1024:
        raise ValidationError("Image file too large ( > 5mb )")


class SettingsForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'status', 'description', 'tags']

    avatar = forms.ImageField(required=False, validators=[validate_max_size])
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)


class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'
        exclude = ['owner']

    picture = forms.ImageField(required=False, validators=[validate_max_size])


class CharacterRemoveForm(ModelForm):
    class Meta:
        model = Character
        fields = 'id'
