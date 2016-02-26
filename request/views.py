import json
from django.http import HttpResponse, Http404
from django.views.generic import View, ListView
from django.contrib.auth.models import User

from models import Request


class HandleOrderingMixin(object):

    ordering = ['-timestamp', ]

    def get_ordering(self):
        '''
        Return the fields for ordering the queryset.
        '''
        ordering = self.ordering
        return tuple(ordering)


class RequestListView(HandleOrderingMixin, ListView):
    '''
    Render page with 10 http requests and return http request count.
    '''
    model = Request
    paginate_by = 10
    template_name = 'request.html'

    def get_queryset(self):
        queryset = super(RequestListView, self).get_queryset()
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RequestListView, self).get_context_data(**kwargs)
        context['request_counter'] = Request.objects.count()
        return context


class RequestCounterView(HandleOrderingMixin, View):
    '''
    Updateing Request objects.
    '''

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = {}
            mimetype = 'application/json'
            queryset = Request.objects.filter(viewed=False)
            context['request_counter'] = queryset.count()

            if self.request.GET.get('viewed') == 'true':
                queryset.update(viewed=True)
                queryset = Request.objects.all()
                context['request_counter'] = 0

            ordering = self.get_ordering()
            if ordering:
                queryset = queryset.order_by(*ordering)

            data = []
            for obj in queryset[:10]:
                data.append({
                    'title': obj.__str__(),
                    'timestamp': obj.timestamp.strftime('%Y-%m-%d %H:%M'),
                    'viewed': unicode(obj.viewed),
                    'id': obj.id,
                })

            context['object_list'] = data
            data = json.dumps(context)
            return HttpResponse(data, mimetype)
        raise Http404