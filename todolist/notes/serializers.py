from .models import *
from .util import *
import json

def note_encoder(note, request=None):
    tl = note.tasklist
    if request:
        tlj = TaskList_Proxy.get(request, tl)
        if tlj.status_code < 400:
            tl = json.loads(tlj.content.decode('utf-8'))
        else:
            raise Exception('Not allowed')
    return {'id': note.id, 'title': note.title,
            'content': note.content,
            'tasklist': tl, 'owner': note.owner.username}
