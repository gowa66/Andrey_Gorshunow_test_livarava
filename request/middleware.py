from django.conf import settings
from django.core.urlresolvers import reverse

from models import Request

class SaveRequestMiddleware(object):
    '''
    Middleware for saving http requests in db
    '''
    def process_request(self, request):

        path_info = request.META['PATH_INFO']

        exlude_list = [reverse('request-counter'),
                       reverse('admin:jsi18n'),
                       settings.MEDIA_URL,
                       settings.STATIC_URL]

        if not any(url in path_info for url in exlude_list):
            new_http_request = Request()
            new_http_request.method = request.META['REQUEST_METHOD']
            new_http_request.path_info = path_info
            new_http_request.server_protocol = request.META['SERVER_PROTOCOL']
            new_http_request.viewed = False
            new_http_request.save()