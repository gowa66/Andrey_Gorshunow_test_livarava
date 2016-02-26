from django.db import models

# Create your models here.

class Request(models.Model):
    '''
    Model for saving request data in db
    '''
    method = models.CharField(max_length=10)
    path_info = models.CharField(max_length=200)
    server_protocol = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Request {0} {1} {2}'.format(
            self.method, self.path_info, self.server_protocol)