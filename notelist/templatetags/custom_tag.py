from django import template
from ..models import Note

register = template.Library()

register.inclusion_tag('custom_tag.html')
def note_by_id(pk):
	return { 'note': Note.objects.get(pk=pk) }