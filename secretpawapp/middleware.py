from django.http import HttpResponseRedirect
from django.shortcuts import render

from secretpaw import settings


class PawgateMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path_info.startswith('/pawgate'):
            try:
                pawgate = request.session['pawgate']
                if not pawgate == hash(settings.PAWGATE_SECRET + settings.SECRET_KEY):
                    return HttpResponseRedirect('/pawgate')
            except KeyError:
                return HttpResponseRedirect('/pawgate')

            if not request.path_info.startswith('/accounts'):
                if request.user.is_authenticated and not request.user.profile.is_verified:
                    return render(request, 'secretpawapp/verification.html', {})

        response = self.get_response(request)
        return response

