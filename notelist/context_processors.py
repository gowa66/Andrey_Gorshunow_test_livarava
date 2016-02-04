from models import Note

def total_note_amount(request):
    return {'total': Note.objects.count()} 
