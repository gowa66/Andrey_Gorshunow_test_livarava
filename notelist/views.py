from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.contrib import messages
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