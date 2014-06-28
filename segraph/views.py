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
                   pic_list:[{pid:122, time:20140503,
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
    gal_list = Gal.objects.filter(gid=request.POST['gid'])
    # check if empty
    if len(gal_list) == 0:
        return HttpResponse(dumps({'code': 'gal not found'}))
    gal_item = gal_list[0]
    gal_json = dumps({ "gid": gal_item.gid,
                       "galname": gal_item.galname})
    return HttpResponse(gal_json)
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
                  "city":"xx", contact:"xx", "galname": "xx"}
      | exception: {"code": "undefined"}

    #POST:
    r_code: json
      | example: {"code": "success"}
      | exception: {"code": "undefined"}
    """
    pic_list = Pic.objects.filter(pid=request.POST['pic'])
    #check if empty
    if len(pic_list) == 0:
        return HttpResponse(dumps({'code': 'pic not found'}))
    pic_item = pic_list[0]

    pic_json = dumps({ "pid": pic_item.pid,
                       "content": pic_item.content,
                       "time": pic_item.time,
                       "uid": pic_item.user.uid,
                       "username": pic_item.user.username,
                       "intro": pic_item.user.intro,
                       "avator": pic_item.user.avator,
                       "city": pic_item.user.city,
                       "contact": pic_item.user.contact,
                       "galname": pic_item.gal.galname})
    return HttpResponse(pic_json)
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
