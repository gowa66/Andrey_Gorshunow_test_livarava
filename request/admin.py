from django.contrib import admin
from django.db.models import Q

from models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'timestamp', )
    date_hierarchy = 'timestamp'

admin.site.register(Request, RequestAdmin)