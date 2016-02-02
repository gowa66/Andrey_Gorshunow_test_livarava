from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Note(models.Model):
    def __unicode__(self):
        return self.text

    text = models.TextField(verbose_name=_("text field"),
    	validators=[MinLengthValidator(10,message=_('Do not allowed to post note shorter that 10 symbols.'))]
        )

    class Meta:
        verbose_name_plural = _("text notes")
    	app_label = 'notelist'