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

def chats(request):
    if request.user.is_authenticated:
        convs=[]
        for chat in request.user.account.chats.all():
            if chat.last_msg:
                convs.append(chat)
        convs.sort(key = lambda x:x.age)
        return redirect('chatroom',room_name=convs[0].group_name)
    else:
        return HttpResponse('notloggedin',status=500)

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

            convs=[]
            for conv in request.user.account.chats.all():
                if conv.last_msg:
                    convs.append(conv)

            convs.sort(key = lambda x:x.age)
            context['convs']=convs
            for member in chat.members.all():
                context['dp_urls'][member.user.username]=member.profile_img_url
        except Chats.DoesNotExist:
            return HttpResponse('chatroomdne',status=500)
        return render(request,'chat.html',context)
    else:
        return HttpResponse('notloggedin',status=500)

def start_chat(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            try:
                member=User.objects.get(username=request.POST['member']).account
            except User.DoesNotExist:
                return HttpResponse("DNE",status=500)
            if member.user == request.user:
                return HttpResponse("self",status=500)
            user=request.user.account
            chat=None
            print(member.name)
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
                chat.last_seen_msg=json.dumps({user.user.username:-1, member.user.username:-1})
                chat.save()
                print(chat.group_name)
            return HttpResponse('/chat/t/'+chat.group_name,status=200)
        else:
            return HttpResponse('notloggedin',status=500)
    else:
        return HttpResponse('invalid-request',status=500)



def get_online(request):
    account=request.user.account
    account.last_active=datetime.utcnow()
    account.save()
    active=[]
    for friend in list(account.followers.all()) + list(account.following.all()):
        if friend.last_active:
            diff=datetime.utcnow()-friend.last_active.replace(tzinfo=None)
            if diff.days<1 and diff.seconds<=15:
                user={}
                user['name']=friend.name
                user['username']=friend.user.username
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
            resp=la.astimezone(timezone.utc).strftime("%b. %d, %Y %I:%M %p")
            if diff.days<1 and diff.seconds<=30:
                resp='Online'
        return HttpResponse(resp,status=200)
    except User.DoesNotExist:
        return HttpResponse('DNE',status=500)


