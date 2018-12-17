from django.http import HttpResponseRedirect
from django.shortcuts import render
from django_registration.backends.activation.views import RegistrationView as BaseRegistrationView

from secretpaw import settings
from secretpawapp.forms import PawgateForm


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
    return render(request, 'secretpawapp/profile.html', {})


