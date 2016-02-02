from django.contrib import admin

from models import Note
from forms import NoteAdmin


# Register your models here.

admin.site.register(Note, NoteAdmin)