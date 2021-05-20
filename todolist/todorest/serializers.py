from json import JSONEncoder
from typing import Any

class TaskListEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(self, o):
            return { 'title': o.title, 'owner': o.owner}
        
        return super().default(o)

class CategoryEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(self, o):
            return { 'title': o.title, 'owner': o.owner, 'description': o.description}
        
        return super().default(o)


class TaskEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(self, o):
            return { 'title': o.title, 
                    'owner_list': o.ownerList, 
                    'description': o.description,
                    'deadline': o.deadline,
                    'category': o.category }
        
        return super().default(o)
