from .models import *


def note_encoder(note):
    return {'id': note.id, 'title': note.title,
            'content': note.content,
            'tasklist': note.tasklist, 'owner': note.owner.username}
