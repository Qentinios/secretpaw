from django.http import HttpResponseRedirect

from secretpaw import settings


class PawgateMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info.startswith('/pawgate'):
            pass

        else:
            try:
                pawgate = request.session['pawgate']
                if not pawgate == hash(settings.PAWGATE_SECRET + settings.SECRET_KEY):
                    return HttpResponseRedirect('/pawgate')
            except KeyError:
                return HttpResponseRedirect('/pawgate')

        response = self.get_response(request)
        return response

