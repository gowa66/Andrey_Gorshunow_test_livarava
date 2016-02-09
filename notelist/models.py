from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete

def image_directory_path(instance, filename):
    """Image upload path"""
    return 'note_{0}/{1}'.format(instance, filename)

# Create your models here.
class Note(models.Model):
    """Notes Model"""
    
    def __unicode__(self):
        return "%s" % unicode(self.text)

    text = models.TextField(
        verbose_name=_("text field"),
        )
    image = models.ImageField(
        upload_to=image_directory_path,
        blank=True,
        null=True,
        )


    class Meta:
         verbose_name_plural = _("text notes")
         app_label = 'notelist'

class Book(models.Model):
    """Book Model"""
    title = models.CharField(max_length=100)
    notes = models.ManyToManyField(Note)
    
    def __unicode__(self):
        return self.title


def note_delete(sender, instance, *args, **kwargs):
    for book in instance.book_set.all():
        if book.notes.count() == 1:
            book.delete()

pre_delete.connect(note_delete, sender=Note)
