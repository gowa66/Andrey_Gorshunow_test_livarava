from django.contrib import admin

from django.core.urlresolvers import reverse
from models import Note, Book, NoteBook
from forms import NoteForm

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    form = NoteForm


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'notes_written')

    def notes_written(self, obj):
        redirect_url = '/admin/notelist/note/'
        extra = "?book__id__exact=%d" % obj.id
        return "<a href='%s'>Notes in this book</a>" % (redirect_url + extra)
    notes_written.allow_tags = True


class NoteBookAdmin(admin.ModelAdmin):
    raw_id_fields = ['note', 'book']

admin.site.register(Book, BookAdmin)
admin.site.register(NoteBook, NoteBookAdmin) 
admin.site.register(Note, NoteAdmin)