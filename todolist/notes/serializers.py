from .models import *
from .util import *
import json

def note_encoder(note, request=None):
    tl = note.tasklist
    if request:
        tl = json.loads(TaskList_Proxy.get(request, tl).content.decode('utf-8'))
    return {'id': note.id, 'title': note.title,
            'content': note.content,
            'tasklist': tl, 'owner': note.owner.username}
