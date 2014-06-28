from json import dumps
from hashlib import sha512
from django.http import HttpResponse
from models import *

def login_view(request):
    """

    """
    user_list=User.objects.filter(username=request.POST['username'])
    if len(user_list)==0:
        return HttpResponse(dumps({'error':'user not found'}))
    if sha512(request.POST['password']+user_list[0].salt).hexdigest()!=user_list[0].hashed_password:
        return HttpResponse(dumps({'error':'incorrect password'}))
    return HttpResponse(dumps({'token':sha512(user_list[0].username).hexdigest()}))


def register_view(request):
    user_list=User.objects.filter(username=request.POST['username'])
    if len(user_list)>0:
        return HttpResponse(dumps({'error':'username already occupied'}))


def user_view(request):
    pass

def gal_view(request):
    pass

def pic_view(request):
    pass

def match_view(request):
    pass