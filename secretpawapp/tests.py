from django.test import TestCase
from django.contrib.auth.models import User

from secretpawapp import forms
from secretpawapp.models import Profile


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.sample_user = User.objects.create(username='alice',
                                               password='secret',
                                               email='example1@example.com')
        self.sample_user2 = User.objects.create(username='bob',
                                                password='swordfish',
                                                email='example2@example.com')
        self.sample_user_profile = Profile.objects.create(user=self.sample_user,
                                                          facebook='https://www.facebook.com/exampleuser')
        self.sample_user_profile2 = Profile.objects.create(user=self.sample_user2,
                                                           facebook='https://www.facebook.com/exampleuser2')


class RegistrationModelTests(RegistrationTestCase):
    def test_new_user_is_inactive(self):
        self.failIf(self.sample_user.is_active)

    def test_user_created(self):
        self.assertEqual(User.objects.count(), 2)

    def test_profile_created(self):
        self.assertEqual(Profile.objects.count(), 2)


class RegistrationFormTests(RegistrationTestCase):

    def test_registration_form(self):
        invalid_data_dicts = [
            # Non-alphanumeric username.
            {
                'data':
                    {'username': 'foo/bar',
                     'email': 'example3@example.com',
                     'password1': 'zaq1@WSX',
                     'password2': 'zaq1@WSX',
                     'facebook': 'https://www.facebook.com/exampleuser3'},
            },
            # Already-existing username.
            {
                'data':
                    {'username': 'alice',
                     'email': 'example4@example.com',
                     'password1': 'zaq1@WSX',
                     'password2': 'zaq1@WSX',
                     'facebook': 'https://www.facebook.com/exampleuser4'},
            },
            # Mismatched passwords.
            {
                'data':
                    {'username': 'foo2',
                     'email': 'example5@example.com',
                     'password1': 'zaq1@WSX',
                     'password2': 'XSW@1qaz',
                     'facebook': 'https://www.facebook.com/exampleuser5'},
            },
            # Duplicated email.
            {
                'data':
                    {'username': 'foo3',
                     'email': 'example1@example.com',
                     'password1': 'zaq1@WSX',
                     'password2': 'zaq1@WSX',
                     'facebook': 'https://www.facebook.com/exampleuser6'},
            },
            # Duplicated facebook.
            {
                'data':
                    {'username': 'foo4',
                     'email': 'example6@example.com',
                     'password1': 'zaq1@WSX',
                     'password2': 'zaq1@WSX',
                     'facebook': 'https://www.facebook.com/exampleuser'},
            },
            # Wrong facebook url.
            {
                'data':
                    {'username': 'foo5',
                     'email': 'example7@example.com',
                     'password1': 'zaq1@WSX',
                     'password2': 'zaq1@WSX',
                     'facebook': 'https://www.test.com'},
            },
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.RegistrationFormUniqueEmailAndFacebook(data=invalid_dict['data'])
            self.failIf(form.is_valid())

        form = forms.RegistrationFormUniqueEmailAndFacebook(data={'username': 'foo5',
                                                                  'email': 'example8@example.com',
                                                                  'password1': 'zaq1@WSX',
                                                                  'password2': 'zaq1@WSX',
                                                                  'facebook': 'https://www.facebook.com/exampleuser7'})

        self.failUnless(form.is_valid())
