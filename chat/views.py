from django.db import reset_queries
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import json
from datetime import datetime,timedelta,timezone
from django.utils import tree
from .models import Chats
from django.contrib.auth.models import User
import hashlib
# Create your views here.
def correct_tz(dt):
    dt=dt.replace(tzinfo=timezone(timedelta(hours=-6,minutes=30)))
    return dt

def chatroom(request,room_name):
    if request.user.is_authenticated:
        try:
            chat=Chats.objects.get(group_name=room_name)
            other=list(filter(lambda x:x.user.username!=request.user.username,list(chat.members.all())))[0]
            context={}
            context['title']=other.name
            context['room_icon']=other.profile_img_url
            context['room_name']=room_name
            context['subtitle']=correct_tz(other.last_active) if other.last_active else ''
            context['data']=json.loads(chat.data)
            context['other']=other.user.username
            context['dp_urls']={}
            context['seen']=json.loads(chat.last_seen_msg)
            for member in chat.members.all():
                context['dp_urls'][member.user.username]=member.profile_img_url
        except Chats.DoesNotExist:
            return HttpResponse('chatroomdne',status=500)
        return render(request,'chat.html',context)
    else:
        return HttpResponse('notloggedin',status=500)

def start_chat(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            try:
                member=User.objects.get(username=request.GET['member']).account
            except User.DoesNotExist:
                return HttpResponse("DNE",status=500)
            user=request.user.account
            chat=None
            for user_chat in user.chats.all():
                if member in user_chat.members.all():
                    chat=user_chat
                    break
            if not chat:
                chat=Chats()
                grp_name=hashlib.md5((member.user.username+user.user.username).encode('utf8'))
                chat.group_name=grp_name.hexdigest()
                chat.save()
                chat.members.add(user)
                chat.members.add(member)
                chat.data='[]'
                chat.save()
                print(chat.group_name)
            return HttpResponse('/chat/t/'+chat.group_name,status=200)
        else:
            return HttpResponse('notloggedin',status=500)
    else:
        return HttpResponse('invalid-request',status=500)



def get_online(request):
    account=request.user.account
    account.last_active=datetime.utcnow();
    account.save();
    active=[]
    for friend in account.friends.all():
        if friend.last_active:
            diff=datetime.utcnow()-friend.last_active.replace(tzinfo=None)
            if diff.days<1 and diff.seconds<=15:
                user={}
                user['name']=friend.account_name
                user['username']=friend.username
                user['profile_img_url']=friend.profile_img_url
                active.append(user)
    return HttpResponse(json.dumps(active))

def get_last_active(request):
    try:
        username=request.GET['username'].strip('"')
        user=User.objects.get(username=username).account
        resp=""
        if user.last_active:
            diff=datetime.utcnow()-user.last_active.replace(tzinfo=None)
            la=correct_tz(user.last_active)
            print(la)
            resp=la.astimezone(timezone.utc).strftime("%b. %d,%Y %I:%M %p")
            if diff.days<1 and diff.seconds<=30:
                resp='Online'
        return HttpResponse(resp,status=200)
    except User.DoesNotExist:
        return HttpResponse('DNE',status=500)


