from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from models import Note

# Create your views here.
class NoteListView(ListView):
	template_name = "home.html"
	model = Note
