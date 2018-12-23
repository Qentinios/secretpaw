from django.http import HttpResponseRedirect
from django.shortcuts import render
from django_registration.backends.activation.views import RegistrationView as BaseRegistrationView

from secretpaw import settings
from secretpawapp.forms import PawgateForm, UserForm, CharacterForm
from secretpawapp.models import Profile, Tag


class RegistrationView(BaseRegistrationView):
    def create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions.

        """
        new_user = form.save()
        new_user.save()

        self.send_activation_email(new_user)

        return new_user


def pawgate(request):
    # redirect to '/' if already passed
    try:
        pawgate = request.session['pawgate']
        if pawgate == hash(settings.PAWGATE_SECRET + settings.SECRET_KEY):
            return HttpResponseRedirect('/')
    except KeyError:
        pass

    if request.method == 'POST':
        form = PawgateForm(request.POST)
        if form.is_valid():
            request.session['pawgate'] = hash(settings.PAWGATE_SECRET + settings.SECRET_KEY)
            return HttpResponseRedirect('/')
    else:
        form = PawgateForm()

    return render(request, 'secretpawapp/pawgate.html', {'form': form})


def profile(request):
    profile_obj = Profile.objects\
        .select_related('user')\
        .prefetch_related('tags')\
        .prefetch_related('characters')\
        .get(user_id=request.user.id)

    tags = Tag.objects.all()
    form_settings = _profile_settings(request, profile_obj)

    return render(request, 'secretpawapp/profile.html', {'form': form_settings, 'profile': profile_obj, 'tags': tags})


def _profile_settings(request, profile_obj):
    if request.method == 'POST' and "settings" in request.POST:
        form_settings = UserForm(request.POST, request.FILES)
        if form_settings.is_valid():
            profile_obj.avatar = form_settings.cleaned_data['avatar']
            profile_obj.description = form_settings.cleaned_data['description']
            profile_obj.status = form_settings.cleaned_data['status']
            profile_obj.tags.set(request.POST.getlist('tags'))
            profile_obj.save()

    else:
        form_settings = UserForm()

    return form_settings


def _profile_characters(request, profile_obj):
    if request.method == 'POST' and "character" in request.POST:
        form_character = CharacterForm(request.POST, request.FILES)
        if form_character.is_valid():
            pass

    else:
        form_character = CharacterForm()

    return form_character
