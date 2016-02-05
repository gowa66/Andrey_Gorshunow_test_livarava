from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver

def image_directory_path(instance, filename):
    return 'note_{0}/{1}'.format(instance, filename)

# Create your models here.
class Note(models.Model):
	def __unicode__(self):
		return "%s" % unicode(self.text)

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

class Book(models.Model):
    notes = models.ManyToManyField(Note, through="NoteBook")


class NoteBook(models.Model):
    note = models.ForeignKey(Note)
    book = models.ForeignKey(Book)


@receiver(post_delete, sender=NoteBook)
def delete_book_without_notes(sender, **kwargs):
    notebook = kwargs['instance']

    try:
        book = notebook.book

        if NoteBook.objects.filter(book=book).count() == 0:
            book.delete()
    except Book.DoesNotExist:
        pass


