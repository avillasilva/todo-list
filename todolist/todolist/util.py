from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
# from django.contrib.auth import login

def generate_user_token(user):
    '''Generates a token that contains the user id. Can be given to the user client to authenticate.
    '''
    return str(user.id)+'/'+str(default_token_generator.make_token(user))

def validate_user_token(token):
    ''' Given a token, get the user and validate.
    Return a pair (User, boolean) indicating the user and if the token is valid.
    '''
    u, t = token.split('/', 1)
    user = User.objects.get(id=u)
    valid = default_token_generator.check_token(user, t)
    return user, valid

def token_or_cookie_required(token_field='TOKEN'):
    '''Decorator that lookup for `token_field` in the request headers.
    If it is present, check if the token is valid and make sure the user is logged in.
    '''
    tk = 'HTTP_' + token_field.upper().replace('-', '_')
    def wrapper(func, *largs, **lkwargs):
        def inner(request, *args, **kwargs):
            token = request.META.get(tk)
            if token:
                user, valid = validate_user_token(token)
                if valid:
                    # login(request, user)
                    request.user = user
                    return func(request, *args, **kwargs)
            return login_required(func, *largs, **lkwargs)(request, *args, **kwargs)
        return inner
    return wrapper
