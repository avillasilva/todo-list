from django.http import HttpResponse
import requests


def fetch_todolist(method, suburl, proxy_url='http://127.0.0.1:8000/todorest/', *args, **kwargs):
    return requests.request(method, proxy_url+suburl, *args, **kwargs)

def proxy_todolist(request, suburl, method=None, *args, **kwargs):
    kwargs.setdefault('data', request.body)
    kwargs.setdefault('headers', request.headers)
    kwargs.setdefault('cookies', request.COOKIES)
    req = fetch_todolist(method or request.method, suburl, *args, **kwargs)
    # req = requests.request(method or request.method, proxy_url+suburl, data=request.POST, headers=request.headers, cookies=request.COOKIES)
    return HttpResponse(req, headers=req.headers, status=req.status_code)

class Proxy_Model_Stub:
    def __init__(self, suburl):
        self.suburl = suburl if suburl.endswith('/') else suburl + '/'
    
    def _proxy_(self, method, suburlid, request, *args, **kwargs):
        return proxy_todolist(request, suburlid, method=method)
    
    def list(self, request):
        return self.get(request, '')
    
    def post(self, request, body): # aka create
        return self._proxy_('POST', self.suburl, request, body=body)
    
    def get(self, request, id): # aka fetch
        return self._proxy_('GET', self.suburl+str(id), request)
    
    def put(self, request, id, body): # aka update
        return self._proxy_('PUT', self.suburl+str(id), request, body=body)
    
    def delete(self, request, id):
        return self._proxy_('DELETE', self.suburl+str(id), request)
    
    def exists(self, request, id):
        return self.get(request, id).status_code < 400


TaskList_Proxy = Proxy_Model_Stub('tasklist')
Task_Proxy = Proxy_Model_Stub('task')
Category_Proxy = Proxy_Model_Stub('category')
