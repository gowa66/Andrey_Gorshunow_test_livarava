import os
import json
import factory
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Request


class MiddlewareHandleTest(TestCase):
    '''
    Testing the SaveRequestMiddleware
    '''
    def test_middleware_handle_storing_request_log(self):
        '''
        Check that the middleware handle and store request at db
        '''
        Request.objects.all().delete()
        self.client.get(reverse('home'))
        self.client.get(reverse('request'))
        self.client.get(reverse('request'))

        self.assertEqual(Request.objects.count(), 3)
        self.assertEqual(Request.objects.first().path_info, reverse('home'))
        self.assertEqual(
            Request.objects.all()[1].path_info, reverse('request'))

class RequestFactory(factory.Factory):
    FACTORY_FOR = Request

    path_info = factory.LazyAttribute(lambda a: '/some-url-{}/'.format(a.id))


class RequestTest(TestCase):
    '''
    Testing response from request-log page
    '''

    def test_exist_request_log_url(self):
        '''
        Check responce status.
        '''
        response = self.client.get(reverse('request'))
        self.assertEqual(response.status_code, 200)

    def test_api_request_count_started(self):
        '''
        Testing API: requests count without log request
        '''
        response = self.client.get(
            reverse('request-counter'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_counter'], 0)

    def test_api_request_count_secont(self):
        '''
        Testing API: request count with 2 requests
        '''
        self.client.get(reverse('home'))
        self.client.get(reverse('home'))
        response = self.client.get(
            reverse('request-counter'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_counter'], 2)

    def test_requests_pagination(self):
        '''
        Test: return 10 latest objects at the page
        '''
        Request.objects.all().delete()

        for pk in xrange(15):
            RequestFactory(id=pk).save_base()

        response = self.client.get(reverse('request'))

        # check count objects at page
        self.assertEqual(len(response.context['object_list']), 10)

        # check sorting objects at page
        obj_list_sorted = Request.objects.all().order_by('-timestamp',)[:10]
        self.assertQuerysetEqual(
            response.context['object_list'],
            [repr(obj) for obj in obj_list_sorted]
        )

    def test_update_viewed_field(self):
        '''
        Emulating GET request and check request_count then emulating
        POST request and after that check request count through GET request
        '''
        Request.objects.all().delete()
        # generate 1 object with viewed=True
        RequestFactory(id=1, viewed=True).save_base()

        # generate 15 objects with viewed=False
        for pk in xrange(2, 17):
            RequestFactory(id=pk).save_base()

        # check request_count through GET request
        response = self.client.get(
            reverse('request-counter'),
            {'viewed': 'false'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_counter'], 15)

        # emulate request when user visiting the page
        response = self.client.get(
            reverse('request-counter'),
            {'viewed': 'true'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check request_count
        self.assertEqual(json.loads(response.content)['request_counter'], 0)