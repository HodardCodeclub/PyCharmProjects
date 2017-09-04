from django.http.response import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from mongoengine import connect

from WebApp.models import User


connect('project1')

# Create your views here.
def hello(request):
    return render(request, 'index.html')

def login(request):
    if(request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_email'] = user.email
            request.session['user_password'] = user.password
            return HttpResponsePermanentRedirect('/accounts/' + user.email[:user.email.find('@')])
        except:
            return HttpResponsePermanentRedirect('/')
    elif(request.method == 'GET'):
        return render(request, 'login.html')

def signup(request):
    if(request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print "{0} - {1}".format(email, password)

        user = User(email=email, password=password)
        user.save()

        res = "A user saved to db\n"
        res += "Email: {} \n".format(user.email)
        res += "Password: {} \n".format(user.password)
        res += "Date: {} \n".format(user.date_modified)

        print res

        request.session['user_email'] = user.email
        request.session['user_password'] = user.password
        return HttpResponsePermanentRedirect('/accounts/' + user.email[:user.email.find('@')])
    elif(request.method == 'GET'):
        return render(request, 'signup.html')

def account(request):
    user = User.objects.get(email=request.session['user_email'], password=request.session['user_password'])
    return render(request, 'user.html', {'user': user})

def readAll(request):
    users = User.objects.all()
    res = "All user: <br>"
    for user in users:
        res += "Email: {0}  Password:{1} <br>".format(user.email, user.password)

    return HttpResponse(res)

def deleteAll(request):
    User.objects.all().delete()
    return HttpResponsePermanentRedirect('/')