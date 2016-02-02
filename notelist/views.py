from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from models import Note
from forms import NoteForm

# Create your views here.
class NoteListView(ListView):
	template_name = "home.html"
	model = Note

class AddNoteView(SuccessMessageMixin, CreateView):
    template_name = 'add_form.html'
    model = Note
    form_class = NoteForm
    success_message = "Note added"

    def get_success_url(self):
        return reverse('add_note')