from json import dumps
from hashlib import sha512
from django.http import HttpResponse
from django.db.models import Max
from random import random
from models import *

def login_view(request): # passed
    """

    """
    user_list=User.objects.filter(username=request.POST['username'])
    if len(user_list)==0:
        return HttpResponse(dumps({'error':'user not found'}))
    if sha512(request.POST['password']+user_list[0].salt).hexdigest()!=user_list[0].hashed_password:
        return HttpResponse(dumps({'error':'incorrect password'}))
    return HttpResponse(dumps({'token':sha512(user_list[0].username).hexdigest()}))


def register_view(request): # buggy
    username=request.POST['username']
    user_list=User.objects.filter(username=username)
    if len(user_list)>0:
        return HttpResponse(dumps({'error':'username already occupied'}))
    if User.objects.count()==0:
        uid=0
    else:
        uid=User.objects.all().aggregate(Max('uid'))['uid__max']+1
    hashed_password=request.POST['password']
    salt=str(random())
    hashed_password=sha512(hashed_password+salt).hexdigest()
    intro=request.POST['intro']
    avatar=request.FILES.items()[0]
    city=request.POST['city']
    contact=request.POST['contact']
    User(uid=uid,username=username,hashed_password=hashed_password,salt=salt,intro=intro,avatar=avatar,city=city,contact=contact).save()
    return HttpResponse(dumps({'token':sha512(username).hexdigest()}))


def user_view(request):
    pass

def gal_view(request):
    pass

def pic_view(request):
    pass

def match_view(request):
    pass