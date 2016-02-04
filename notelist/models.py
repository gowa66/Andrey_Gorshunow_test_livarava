from django.db import models
from django.utils.translation import ugettext_lazy as _


def image_directory_path(instance, filename):
    return 'note_{0}/{1}'.format(instance, filename)

# Create your models here.
class Note(models.Model):
	def __unicode__(self):
		return self.text

	text = models.TextField(verbose_name=_("text field"),
		)
	image = models.ImageField(
		upload_to=image_directory_path,
        blank=True,
        null=True,
        )


	class Meta:
         verbose_name_plural = _("text notes")
         app_label = 'notelist'



