from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate
from django.conf import settings
from django.db import transaction
from django.contrib.auth import logout as _logout
from django.contrib.auth import login as _login
from collections import OrderedDict
import forms
import members.models


def context_processor(request):
    """Run to provide every template context with some standard variables"""
    ctx = {
        'TITLE': 'Iffley Fields Woodcraft Folk Elfins Group'
    }
    ctx['static_url'] = settings.STATIC_URL
    if request.user.is_authenticated():
        ctx['username'] = request.user.username
    return ctx


def dodoc(text):
    if text is None:
        return None, None
    lines = [line.strip() for line in text.split('\n')]
    title = lines[0]
    paragraphs = ['']
    for line in lines[1:]:
        if line != '':
            paragraphs[-1] = line if paragraphs[-1] == '' else paragraphs[-1] + ' ' + line
        else:
            paragraphs = paragraphs + [''] if paragraphs[-1] != '' else paragraphs
    return title, paragraphs


class AuthenticationError(StandardError):
    app = "wfm"


def login_form(request, ctx):
    ctx['authenticationform'] = forms.AuthenticationForm()
    t = loader.get_template('login.html')
    return HttpResponse(t.render(RequestContext(request, ctx)))


def requireSession(view):
    def session_wrapper(request, db=None, ctx=None):
        ctx = {} if ctx is None else ctx
        try:
            doc = view.__doc__ if hasattr(view, '__doc__') else None
            ctx['help_title'], ctx['help_text'] = dodoc(doc)
            if request.user.is_authenticated():
                return view(request, db, ctx)
            elif 'username' in request.POST and 'password' in request.POST: #?move
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        with transaction.commit_on_success():
                            _login(request, user)
                            ctx['app_messages'] = ['Login successful']
                            return _home(request, db, ctx)
                    else:
                        raise AuthenticationError('Login failed: inactive user.')
                else:
                    raise AuthenticationError('Login failed: non-existent username or incorrect password')
            else:
                raise AuthenticationError('Not currently authenticated')
        except AuthenticationError, e:
            ctx['app_messages'] = [e.message or str(e)]
            return login_form(request, ctx)
        except StandardError, e:
            ctx['app_messages'] = [e.message or str(e)]
            return _home(request, db, ctx)
        except Exception, e:
            raise e

    return session_wrapper


def _home(request, db=None, ctx=None):
    t = loader.get_template('home.html')
    ctx['summary'] = OrderedDict([
        ('Waiting list', len(members.models.Member.waiters())),
        ('Elfins', len(members.models.Member.elfins())),
        ('Woodchips', len(members.models.Member.woodchips())),
        ('Carers', len(members.models.Member.carers())),
    ])
    return HttpResponse(t.render(RequestContext(request, ctx)))


def home(request, db=None, ctx={}):
    """ Home
    Summary
    """
    return _home(request, db, ctx)


@requireSession
def logout(request, db=None, ctx={}):
    """You have been logged out.

    Login to proceed.
    """
    session_id = request.session.session_key
    _logout(request)
    request.session.logged_out = True
    ctx['app_messages'] = ['You have been logged out']

    return _home(request, db, ctx)

@requireSession
def login(request, db=None, ctx={}):
    """Login

    Enter Authentication details.
    """
    return _home(request, db, ctx)


def _carers(request, db=None, ctx={}):
    t = loader.get_template('carers.html')
    ctx['carers'] = members.models.Member.carers()
    return HttpResponse(t.render(RequestContext(request, ctx)))

@requireSession
def carers(request, db=None, ctx={}):
    """Carers

    Carers with expiry dates.
    """
    return _carers(request, db, ctx)
