from django.http.response import JsonResponse
from django.shortcuts import render
from groups.models import Group
from users.models import Account
from post.models import Post
from django.urls import reverse
from django.http import HttpResponseNotFound

# Create your views here.
def index(request):
    if request.user.is_staff:
        context = {
            'active_tab':'dashboard'
        }
        return render(request,'index.html',context)
    return HttpResponseNotFound("Page Not Found")

def accounts(request):
    if request.user.is_staff:
        res = [];
        for acc in Account.objects.all():
            if acc == request.user.account:
                continue
            ele ={'title':acc.name,'subtitle':acc.designation,'img':acc.profile_img_url,
            'url':reverse('account',args=[acc.user.username]),'username':acc.user.username,'id':acc.id}
            res.append(ele)
            res.sort(key=lambda x: x.get('title'))
        context = {
            'active_tab':'accounts',
            'acc':res,
        }
        return render(request,'accounts.html',context)
    return HttpResponseNotFound("Page Not Found")

def posts(request):
    if request.user.is_staff:
        res = [];
        for post in Post.objects.all():
            ele ={'author':post.author.name,'time':post.datetime,
            'authorURL':reverse('account',args=[post.author.user.username]),
            'report':post.reports.all().count(),
            'url':'/post-detail/'+ str(post.id),'likes':post.likes.all().count(),'id':post.id}
            res.append(ele)
            res.sort(key=lambda x: x.get('time'), reverse=True)
            res.sort(key=lambda x: x.get('report'), reverse=True)
        context = {
            'active_tab':'posts',
            'posts':res,
        }
        return render(request,'allposts.html',context)
    return HttpResponseNotFound("Page Not Found")

def groups(request):
    if request.user.is_staff:
        res = [];
        for group in Group.objects.all():
            ele={'title':group.title,'subtitle':str(group.member_count)+' members',
            'img':'','url':reverse('groups:group',args=[group.id]),'id':group.id}
            ele['joined']=request.user.account in group.members.all()
            if group.cover_image:
                ele['img']=group.cover_image.url
            res.append(ele)
        context = {
            'active_tab':'groups',
            'groups':res,
        }
        return render(request,'allgroups.html',context)
    return HttpResponseNotFound("Page Not Found")

def delete_account(request,id):
    if request.user.is_staff:
        try:
            Account.objects.get(id=id).delete()
            return JsonResponse({"message":"deleted the account","status":200})
        except:
            return JsonResponse({"message":"unable to delete this account","status":400})
    return HttpResponseNotFound("Page Not Found")

def delete_post(request,id):
    if request.user.is_staff:
        try:
            Post.objects.get(id=id).delete()
            return JsonResponse({"message":"deleted the post","status":200})
        except:
            return JsonResponse({"message":"unable to delete this post","status":200})
    return HttpResponseNotFound("Page Not Found")

def delete_group(request,id):
    if request.user.is_staff:
        try:
            Group.objects.get(id=id).delete()
            return JsonResponse({"message":"deleted the group","status":200})
        except:
            return JsonResponse({"message":"unable to delete this group","status":200})
    return HttpResponseNotFound("Page Not Found")