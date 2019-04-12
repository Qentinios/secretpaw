from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_registration.backends.activation.views import RegistrationView as BaseRegistrationView

from secretpaw import settings
from secretpawapp.forms import PawgateForm, SettingsForm, CharacterForm, CharacterRemoveForm, GiftForm
from secretpawapp.helpers import encode_profile_url, decode_profile_url
from secretpawapp.models import Profile, Tag, CharacterNSFWTypes, Character, Gift


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


@login_required
def profile(request):
    profile_obj = Profile.objects\
        .select_related('user')\
        .prefetch_related('tags')\
        .get(user_id=request.user.id)

    form_settings = _form_settings(request, profile_obj)
    form_character = _form_character(request, profile_obj)
    _form_character_remove(request)
    form_gift = _form_gift(request)

    tags = Tag.objects.all()
    nsfw_types = CharacterNSFWTypes.objects.all()
    characters = Character.objects.filter(owner=profile_obj)
    gift_from_you = Gift.objects.get(giver=profile_obj)
    gift_for_you = Gift.objects.get(recipient=profile_obj)

    if gift_from_you:
        rewarded_profile_url = encode_profile_url(gift_from_you.recipient.user_id)
    else:
        rewarded_profile_url = None

    profile_url = encode_profile_url(request.user.id)
    sex_choices = Character.SEX_CHOICES

    return render(request, 'secretpawapp/profile.html', {
        'form_settings': form_settings, 'form_character': form_character, 'form_gift': form_gift, 'share_link': profile_url,
        'profile': profile_obj, 'characters': characters, 'tags': tags, 'nsfw_types': nsfw_types, 'sex_choices': sex_choices,
        'gift_from_you': gift_from_you, 'gift_for_you': gift_for_you, 'rewarded_profile_url': rewarded_profile_url
    })


def visitor(request, share_link):
    user_id = decode_profile_url(share_link)

    profile_obj = Profile.objects\
        .select_related('user')\
        .prefetch_related('tags')\
        .get(user_id=user_id)

    tags = Tag.objects.all()
    nsfw_types = CharacterNSFWTypes.objects.all()
    characters = Character.objects.filter(owner=profile_obj)
    sex_choices = Character.SEX_CHOICES

    return render(request, 'secretpawapp/visitor.html', {
        'profile': profile_obj, 'characters': characters, 'tags': tags, 'nsfw_types': nsfw_types, 'sex_choices': sex_choices,
    })


def _form_settings(request, profile_obj):
    if request.method == 'POST' and "settings" in request.POST:
        form_settings = SettingsForm(request.POST, request.FILES)
        if form_settings.is_valid():

            image = form_settings.cleaned_data['avatar']
            if image:
                profile_obj.avatar = image
            profile_obj.description = form_settings.cleaned_data['description']
            profile_obj.status = form_settings.cleaned_data['status']
            profile_obj.tags.set(request.POST.getlist('tags'))
            profile_obj.save()

            messages.info(request, 'Profile details updated.')

            return HttpResponseRedirect('/')

    else:
        form_settings = SettingsForm()

    return form_settings


def _form_character(request, profile_obj):
    if request.method == 'POST' and "character" in request.POST:
        form_character = CharacterForm(request.POST, request.FILES)
        if form_character.is_valid():
            character_id = request.POST['character_id']

            if character_id:
                try:
                    character_obj = Character.objects\
                        .prefetch_related('nsfw')\
                        .get(id=character_id)
                except Character.DoesNotExist:
                    return HttpResponseRedirect('/')
                messages.info(request, 'Character updated.')
            else:
                character_obj = Character()
                messages.success(request, 'Character created.')

            image = form_character.cleaned_data['picture']
            if image:
                character_obj.picture = image

            character_obj.owner = profile_obj
            character_obj.picture_author = form_character.cleaned_data['picture_author']
            character_obj.name = form_character.cleaned_data['name']
            character_obj.age = form_character.cleaned_data['age']
            character_obj.race = form_character.cleaned_data['race']
            character_obj.sex = form_character.cleaned_data['sex']
            character_obj.tag = form_character.cleaned_data['tag']
            character_obj.description = form_character.cleaned_data['description']
            character_obj.hints = form_character.cleaned_data['hints']
            character_obj.save()
            character_obj.nsfw.set(request.POST.getlist('nsfw[]'))
            character_obj.save()

            return HttpResponseRedirect('/')

    else:
        form_character = CharacterForm()

    return form_character


def _form_character_remove(request):
    if request.method == 'POST' and "character_delete" in request.POST:
        form_character_remove = CharacterRemoveForm(request.POST)
        if form_character_remove.is_valid():
            character_id = request.POST['character_id']

            if character_id:
                try:
                    Character.objects\
                        .get(id=character_id)\
                        .delete()
                except Character.DoesNotExist:
                    pass
                messages.warning(request, 'Character deleted.')

    return HttpResponseRedirect('/')


def _form_gift(request):
    if request.method == 'POST' and "gift" in request.POST:
        form_gift = GiftForm(request.POST, request.FILES)
        if form_gift.is_valid():
            gift = Gift.objects\
                .get(giver=request.user.id)

            image = form_gift.cleaned_data['picture']
            if image:
                gift.picture = image
            gift.wishes = form_gift.cleaned_data['wishes']
            gift.save()
            messages.success(request, 'Gift has been send for approval.')

            return HttpResponseRedirect('/')

    else:
        form_gift = CharacterForm()

    return form_gift

