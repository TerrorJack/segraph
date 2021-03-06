from json import dumps
from hashlib import sha512
from django.http import HttpResponse
from django.db.models import Max
from random import random
from base64 import standard_b64encode
from time import strftime
from models import *

def std_sha512(s):
    return sha512(s).hexdigest()

def login_view(request): # passed
    """

    """
    user_list=User.objects.filter(username=request.POST['username'])
    if len(user_list)==0:
        return HttpResponse(dumps({'code':'user not found'}))
    if std_sha512(request.POST['password']+user_list[0].salt)!=user_list[0].hashed_password:
        return HttpResponse(dumps({'code':'incorrect password'}))
    return HttpResponse(dumps({'token':std_sha512(user_list[0].username)}))


def register_view(request): # passed
    username=request.POST['username']
    user_list=User.objects.filter(username=username)
    if len(user_list)>0:
        return HttpResponse(dumps({'error':'username already occupied'}))
    uid=User.next()
    hashed_password=request.POST['password']
    salt=str(random())
    hashed_password=std_sha512(hashed_password+salt)
    intro=request.POST['intro']
    avatar=request.FILES.values()[0]
    city=request.POST['city']
    contact=request.POST['contact']
    user=User(uid=uid,username=username,hashed_password=hashed_password,salt=salt,intro=intro,avatar=avatar,city=city,contact=contact)
    user.save()
    return HttpResponse(dumps({'token':std_sha512(username)}))


def user_view(request): # passed
    """
    get the user information which included name, infor, Pic.

    Params:
    -----------
    GET #
    uid: int

    Return:
    -------
    user_json: json
      | example: { uid:1, username:"xxx", intro:"xxx", avatar:=i213adskfa,
                   city:"xxx", contact:"xxx",
                   pic_list:[{pid:122, time:20140503,
                   galname:"xx", content:iasdfadfas}],{..}}
    """
    if request.method=='GET':
        user_list=User.objects.filter(uid=int(request.GET['uid']))
        if len(user_list)==0:
            return HttpResponse(dumps({'code':'user not exist'}))
        user=user_list[0]
        json_pic_list=[{'pid':pic.pid,'time':pic.time,
                        'galname':pic.gal.galname,
                        'content':standard_b64encode(pic.content.read())} for pic in Pic.objects.filter(user=user)]
        return HttpResponse(dumps({'uid':user.uid,'username':user.username,'intro':user.intro,
                                   'avatar':standard_b64encode(user.avatar.read()),
                                   'city':user.city,'contact':user.contact,'pic_list':json_pic_list}))
    else:
        return HttpResponse(dumps({'code':'undefined'}))

def userprofile_view(request): #passed
    """
    get/update the personal profile which included name, infro.

    Params:
    -----------
    GET#
    uid: int

    POST#
    uid: int
    username: str
    intro: str
    city: str
    contact: str

    Returns
    -------
    GET#
    userprofile_json: json
      | example: {"uid":1, "username":"xx", "infor":"xxx"}
    POST#
    r_code: json
      | example: {"code":"success"}
    """
    if request.method=='GET':
        user=User.objects.get(uid=int(request.GET['uid']))
        return HttpResponse(dumps({'uid':user.uid,'username':user.username,
                                   'intro':user.intro,'avatar':standard_b64encode(user.avatar.read()),
                                   'city':user.city,'contact':user.contact}))
    elif request.method=='POST':
        user=User.objects.get(uid=int(request.POST['uid']))
        user.username=request.POST['username']
        user.intro=request.POST['intro']
        user.city=request.POST['city']
        user.contact=request.POST['contact']
        return HttpResponse(dumps({'code':'success'}))
    else:
        return HttpResponse(dumps({'code':'undefined'}))

def gal_view(request): #passed
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

def pic_new_view(request): #passed
    """
    insert pic

    Params:
    -------
    content: FILE
    uid: int
    galname: str
    
    """
    content = request.FILE.values()[0]
    uid = int(request.POST['uid'])
    galname =  request.POST['galname']

    gal_list=Gal.objects.filter(galname=galname)
    if len(gal_list)==0:
        gid=Gal.next()
        gal=Gal(gid=gid,galname=galname)
        gal.save()
    else:
        gal=gal_list[0]
    
    user=User.objects.get(uid=uid)
    time=strftime('%Y%m%d')

    pid=Pic.next()

    Pic(pid=pid,time=time,user=user,gal=gal,content=content).save()

    return HttpResponse(dumps({"code":"success"}))

    
def pic_view(request):
    """
    get a single picture by pid

    Params:
    -------
    #GET
    pid: int

    Returns:
    --------
    #GET
    pic_json: json
      | example: {"pid":"1", "time":"20140404", "content":"xxx","uid":"1",
                  "username":"xx", "intro":"xxx", avatar:"base64xxxxx",
                  "city":"xx", contact:"xx", "galname": "xx"}
      | exception: {"code": "undefined"}
    """
    pic_list = Pic.objects.filter(pid=request.POST['pic'])
    #check if empty
    if len(pic_list) == 0:
        return HttpResponse(dumps({'code': 'pic not found'}))
    pic_item = pic_list[0]

    pic_json = dumps({ "pid": pic_item.pid,
                       "content": pic_item.content.read(),
                       "time": pic_item.time,
                       "uid": pic_item.user.uid,
                       "username": pic_item.user.username,
                       "intro": pic_item.user.intro,
                       "avatar": pic_item.user.avatar.read(),
                       "city": pic_item.user.city,
                       "contact": pic_item.user.contact,
                       "galname": pic_item.gal.galname})
    return HttpResponse(pic_json)

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
    # 2333 this is a trivial function!!!
    pics = User.objects.all()
    pic_list = [ {"pid": pic.pid,
                  "content": pic.content.read(),
                  "time": pic.time,
                  "uid": pic.user.uid,
                  "username": pic.user.username,
                  "intro": pic.user.intro,
                  "avatar": pic.user.avatar.read(),
                  "city": pic.user.city,
                  "contact": pic.user.contact,
                  "galname": pic.gal.galname} for pic in pics ]
    pic_json = dumps(pic_list)
    return HttpResponse(pic_json)
