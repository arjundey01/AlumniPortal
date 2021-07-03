import json
from groups.forms import GroupForm
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Group
from post.forms import PostForm

@login_required
def all_groups(request):
    groups=Group.objects.all()
    return render(request, "all_groups.html", context={'groups':groups})

def group(request,id):
    group = get_object_or_404(Group,id=id)
    return render(request,'group.html',{'group':group,'postform': PostForm })
    
def create_group(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/groups/')
    return HttpResponse('Bad Request',status=400)

def delete_group(request,id):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        group = get_object_or_404(Group, id= id)
        group.delete()
        return HttpResponse('Success',status=200)
    return HttpResponse('Bad Request',status=400)

def rename_group(request, id):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        if request.POST.get('title'):
            group = get_object_or_404(Group, id= id)
            group.title = request.POST.get('title')
            group.save()
            return HttpResponse('Success',status=200)
    return HttpResponse('Bad Request',status=400)

def change_cover_group(request, id):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=get_object_or_404(Group,id=id))
        if form.is_valid():
            form.save()
            return HttpResponse('Success',status=200)
    return HttpResponse('Bad Request',status=400)

def join_group(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            group = get_object_or_404(Group, id=id)
            group.members.add(request.user.account)
            return HttpResponse('Success',status=200)
        else:
            return HttpResponse('Bad Request',status=400)
    return HttpResponse('Unauthorized', status=401)

def leave_group(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            group = get_object_or_404(Group, id=id)
            group.members.remove(request.user.account)
            return HttpResponse('Success',status=200)
        else:
            return HttpResponse('Bad Request',status=400)
    return HttpResponse('Unauthorized', status=401)

def get_members(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            group = get_object_or_404(Group, id=id)
            members={'alumni':[],'common':[],'other':[]}
            for member in group.members.all():
                m = {}
                m['username']=member.user.username
                m['profile_img']=member.profile_img_url
                m['name']=member.name
                if member.user.id == request.user.id:
                    m['is_followed']=True
                    members['common'].append(m)
                    continue
                m['is_followed']=member in request.user.account.following.all()
                if member.is_alumni:
                    members['alumni'].append(m)
                else:
                    ctr=0
                    for grp in request.user.account.groups.all():
                        if member in grp.members.all() and grp.id!=group.id:
                            ctr+=1
                    if ctr:
                        members['common'].append(m)
                    else:
                        members['other'].append(m)
            return HttpResponse(json.dumps(members),status=200)
        else:
            return HttpResponse('Bad Request',status=400)
    return HttpResponse('Unauthorized', status=401)


 