# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.core.urlresolvers import reverse

from models import Note
from forms import NoteForm
# Create your tests here.


class TextNoteTest(TestCase):   
    def test_unicode_representation(self):
        note = Note(text="MY ENTRY TITLE")
        self.assertEqual(unicode(note), note.text)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Note._meta.verbose_name_plural), "text notes")


class TestHome(TestCase):
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