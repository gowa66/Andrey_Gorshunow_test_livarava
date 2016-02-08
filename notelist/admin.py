from django.contrib import admin
from models import Note, Book

class NoteBookAdmin(admin.TabularInline):
    model = Book.notes.through
 
 
class NoteAdmin(admin.ModelAdmin):
    inlines = [
        NoteBookAdmin,
    ]


class BookAdmin(admin.ModelAdmin):
    inlines = [
        NoteBookAdmin,
    ]
    exclude = ('notes',)


admin.site.register(Note, NoteAdmin)
admin.site.register(Book, BookAdmin)