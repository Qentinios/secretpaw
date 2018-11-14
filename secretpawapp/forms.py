from django.core.validators import RegexValidator
from django_registration.forms import RegistrationFormUniqueEmail
from django import forms

from secretpawapp.models import Profile


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
