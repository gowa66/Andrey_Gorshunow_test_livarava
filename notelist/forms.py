from django.forms import ModelForm, CharField, Textarea
from django.utils.encoding import smart_text
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from models import Note

class UpperCaseField(CharField):
    def to_python(self, value):
        if value in self.empty_values:
            return ''
        return smart_text(value.upper())

class NoteForm(ModelForm):

	text = UpperCaseField(
		widget=Textarea, 
		required=True, 
		validators=[MinLengthValidator(10,message=_('Do not allowed to post note shorter that 10 symbols.'))]
        )
	
	
	class Meta:
		model = Note
		fields = ['text', 'image']
