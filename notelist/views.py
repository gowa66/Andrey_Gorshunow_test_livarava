from django.core.urlresolvers import reverse
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.contrib import messages
from django.template import loader
from django.template import RequestContext
import json
from models import Note
from forms import NoteForm
from random import randint

# Create your views here.
class NoteListView(ListView):
	template_name = "home.html"
	model = Note

class AddNoteView(SuccessMessageMixin, CreateView):
	template_name = 'add_form.html'
	model = Note
	form_class = NoteForm
	message = _("Note added")
	success_message = message

	def form_invalid(self, form):
		response = super(AddNoteView, self).form_invalid(form)
		if self.request.is_ajax():
			errors = {'errors': form.errors}
			return JsonResponse(errors)
		else:
			return response

	def form_valid(self, form):
		response = super(AddNoteView, self).form_valid(form)
		if self.request.is_ajax():
			data = {
				'message': str(self.message),
				'notes_count': unicode(Note.objects.count()),
			}
			storage = messages.get_messages(self.request)
			del storage._queued_messages[0]
			json_response = JsonResponse(data)
			return json_response
		else:
			return response

	def get_success_url(self):
		return reverse('add_note')

class RandomNoteView(View):

    def get_random_note(self):
        last = Note.objects.count() - 1
        random_index = randint(0, last)
        return Note.objects.all()[random_index]

    def get(self, request):
        response = HttpResponse()
        response['Content-Type'] = 'application/json'
        response['Access-Control-Allow-Origin'] = '*'
        if Note.objects.count() < 1:
            content = {'result': 'failure', 'msg': 'No text notes'}
        else:
            t = loader.get_template('note.html')
            ctx = RequestContext(request, {'note': self.get_random_note()})
            random_note_repr = t.render(ctx)
            content = {'result': 'success', 'random_note': unicode(random_note_repr)}
        response.content = json.dumps(content)
        return response


class WidgetView(TemplateView):
    template_name = "widget.html"

    