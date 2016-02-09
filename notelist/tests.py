# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.http import HttpRequest
from StringIO import StringIO
from PIL import Image
import json

from models import Note, Book
from forms import NoteForm
from context_processors import total_note_amount
# Create your tests here.


class TextNoteTest(TestCase):
    """Testing Note model"""
    def test_unicode_representation(self):
        note = Note(text="MY ENTRY TITLE")
        self.assertEqual(unicode(note), note.text)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Note._meta.verbose_name_plural), "text notes")


class TestHome(TestCase):
    """Testing page with text notes list"""
    def setUp(self):
        Note.objects.get_or_create(
            text="TEST NOTE 1")
        Note.objects.get_or_create(
            text="TEST NOTE 2")
        self.client = Client()
        self.url = reverse('home')

    def test_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')

    def test_quesy_set(self):
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            Note.objects.all(),
            [
                repr(response.context['object_list'][0]),
                repr(response.context['object_list'][1])
            ],
            ordered=False
        )

    def test_no_text_notes(self):
        Note.objects.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, 'No text notes.')

class NoteAddTest(TestCase):
    """Testing for adding note"""
    def test_blank_form(self):
        form = NoteForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,  {'text': [u'This field is required.']})

    def test_valid_form(self):
        form = NoteForm({"text": "TEST NOTE TEST NOTE"})
        self.assertTrue(form.is_valid())
        note = form.save()
        self.assertEqual(note.text, "TEST NOTE TEST NOTE") 
    
    def test_shorter_10_symbols(self):
        form = NoteForm({"text": "Test"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
                         {'text': [u'Do not allowed to post note shorter that 10 symbols.']})

class CustoFormTest(TestCase):
    """Testing custom form"""
    def test_uppercase_note_adding(self):
        uppercase_note = 'TEST UPPER TEXT NOTE.'
        self.client.post(reverse('add_note'), {'text': uppercase_note})
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)
        note_5 = resp.context['object_list'][0]
        self.assertEqual(note_5.text, uppercase_note)

    def test_lowercase_note_adding(self):
        lowercase_note = 'test lower text note.'
        uppercase_result = lowercase_note.upper()
        self.client.post(reverse('add_note'), {'text': lowercase_note})
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)
        note_5 = resp.context['object_list'][0]
        self.assertEqual(note_5.text, uppercase_result)

class ContextProcessorsTest(TestCase):
    """Test for note count context processor"""
    fixtures = ['initial_data.json']

    def test_processor(self):
        """Test groups processor"""
        request = HttpRequest()
        data = total_note_amount(request)
        self.assertEqual(data['total'], 5)

class AjaxTest(TestCase):
    """Testing for adding note view with AJAX"""
    def setUp(self):
        self.client = Client()
        self.url = reverse('add_note')
        self.file_obj = StringIO()
        self.image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
        self.image.save(self.file_obj, 'png')
        self.file_obj.name = 'test.png'
        self.file_obj.seek(0)

    def test_ajax_post(self):
        response = self.client.post(self.url,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_ajax_form_valid(self):
        response = self.client.post(self.url,
                                    {'text': 'TEST TEXT TEST TEXT', 'image': self.file_obj,},
                                    format='json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(isinstance(response, JsonResponse))
        succes_message = json.dumps(
            {u'message': u'Note added', u'notes_count': u'1'}
             )
        self.assertJSONEqual(succes_message, response.content)

    def test_ajax_post_shorter_then_10_symbols(self):
        response = self.client.post(
            self.url,
            {
                'text': 'Test',
                'image': self.file_obj,
            },
            format='json', HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(isinstance(response, JsonResponse))
        error_message = json.dumps(
            {"errors": {"text": ["Do not allowed to post note shorter that 10 symbols."]}}
            )
        self.assertJSONEqual(error_message, response.content)

    def test_ajax_upload_valid_image(self):
        not_image = StringIO()
        not_image.write('First line.\n')
        not_image.name = 'not_image.file'
        not_image.seek(0)
        response = self.client.post(
            self.url,
            {
                'text': 'Test Text Test Text',
                'image': not_image,
            },
            format='json', HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(isinstance(response, JsonResponse))
        error_message = json.dumps(
            {'errors': {'image': [(
                    'Upload a valid image. The file you '
                    'uploaded was either not an image or '
                    'a corrupted image.')]}})
        self.assertJSONEqual(error_message, response.content)

class TestWidgetPage(TestCase):
    """Testing page with widget"""
    def setUp(self):
        self.client = Client()
        self.url = reverse('widget')

    def test_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'widget.html')

class TestWidget(TestCase):
    """Testing widget with random text note"""
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('random_note')
        self.response = self.client.get(self.url)
        self.notes = [object.text for object in Note.objects.all()]

    def test_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_widget_content(self):
        self.assertIn(
            self.response.content.split('<td>')[1].split('</td>')[0],
            self.notes
        )

class BookAutodeleteTest(TestCase):
    """Testing book authomatically delete after last note is deleted"""
    def test_book_autodelete(self):
        note1 = Note(text='text')
        note1.save()
        note2 = Note(text='text')
        note2.save()
        book = Book(title='title')
        book.save()
        book.notes.add(*[note1, note2])
        note1.delete()
        self.assertTrue(Book.objects.all())
        note2.delete()
        self.assertFalse(Book.objects.all())