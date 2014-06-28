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
    """
    get the user information which included name, infor, Pic.

    Params:
    -----------
    uid: int

    Return:
    -------
    user_json: json
      | example: { uid:1, username:"xxx", intro:"xxx", avatar:=i213adskfa,
                   city:"xxx", contact:"xxx",
                   pic_list:[{pid:122, time:20140503, user:"xx",
                   galname:"xx", content:iasdfadfas}],{..}}
    """
    pass

def userproflie_view(request):
    """
    get/update the personal profile which included name, infro.

    Params:
    -----------
    GET#
    uid: int

    POST#
    name: str
    infor: str

    Returns
    -------
    GET#
    userprofile_json: json
      | example: {"uid":1, "name":"xx", "infor":"xxx"}
    POST#
    r_code: json
      | example: {"code":"success"}
    """
    pass

def gal_view(request):
    """
    get the gal name by gid

    Params:
    -------
    gid: int

    Returns:
    --------
    gal_json: json
      | example: {"gid":"1", "galname":"xx"}
      | exception: {"code": "undefined"}
    """
    pass

def pic_view(request):
    """
    get a single picture by pid

    Params:
    -------
    #GET
    pid: int

    #POST
    uid: int
    content: base64
    
    Returns:
    --------
    #GET
    pic_json: json
      | example: {"pid":"1", "time":"20140404", "content":"xxx","uid":"1",
                  "username":"xx", "intro":"xxx", avator:"base64xxxxx",
                  "city":"xx", contact:"xx"}
      | exception: {"code": "undefined"}

    #POST:
    r_code: json
      | example: {"code": "success"}
      | exception: {"code": "undefined"}
    """
    pass

def match_view(request):
    """
    get the suitable coser with the KNN Algorithm ( really?23333

    Params:
    -------
    uid: int

    Returns:
    user_list: json
      | example: [{ uid:1, username:"xxx", intro:"xxx", avatar:="base64",
                   city:"xxx", contact:"xxx",
                   pic_suited:{pid:122, time:20140503, user:"xx",
                   galname:"xx", content:iasdfadfas} },..,{..}]
      | exception: {"code": "undefined"}
    """
    pass
