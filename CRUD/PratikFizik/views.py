from django.shortcuts import render


from PratikFizik.models import Account
from mongoengine import connect

# Create your views here.
connect("pratikFizik")

def login(request):
    if request.method == 'GET':
        _name = request.GET.get('name')
        _password = request.GET.get('password')
        _chapters = request.GET.get('chapters')
        try:
            _account = Account.objects.get(name=_name, password=_password, chapters=_chapters)
            print _account
        except:
            return {}

def signup(request):
    if request.method == 'GET':
        _name = request.GET.get('name')
        _password = request.GET.get('password')
        _chapters = request.GET.get('chapters')

        print "{0}-{1}-{2}".format(_name, _password, str(_chapters))

        _account = Account(name=_name, password=_password, chapters=_chapters)
        _account.save()