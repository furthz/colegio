
from threading import local
_thread_locals = local()

def get_current_request():
    """ returns the HttpRequest object for this thread """
    return getattr(_thread_locals, "request", None)

def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


def get_current_colegio():
    return getattr(_thread_locals, "request", None)


def get_current_colegio():
    request = get_current_request()
    if request.session.get('colegio'):
        id = request.session.get('colegio')
        return id


class ThreadLocalMiddleware(object):
    """ Middleware that adds the HttpRequest object
        to thread local storage """
    def process_request(self, request):
        _thread_locals.request = request

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response

def get_current_userID():
    request = get_current_request()
    if request.session.get('user'):
        iduser = request.session.get('user')
        return iduser

