from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from events.models import Event
from groups.models import Group
from users.models import Account
from post.models import Post
from faq.models import Question
from django.urls import reverse
from django.http import HttpResponseNotFound

# Create your views here.
def index(request):
    if request.user.is_staff:
        return redirect('/admin/accounts/')
    return redirect('/signin/')

def accounts(request):
    if request.user.is_staff:
        res = []
        for acc in Account.objects.all():
            ele ={'title':acc.name,'subtitle':acc.designation,'img':acc.profile_img_url,
            'url':reverse('account',args=[acc.user.username]),'username':acc.user.username,'id':acc.id}
            res.append(ele)
        res.sort(key=lambda x: x.get('title'))
        context = {
            'active_tab':'accounts',
            'acc':res,
        }
        return render(request,'admin-accounts.html',context)
    return redirect('/signin/')

def events(request):
    if request.user.is_staff:
        res = []
        for event in Event.objects.all():
            res.append(event)
            res.sort(key=lambda x: x.event_date, reverse=True)
        context = {
            'active_tab':'events',
            'events':res,
        }
        return render(request,'admin-events.html',context)
    return redirect('/signin/')

def faqs(request):
    if request.user.is_staff:
        res = []
        for faq in Question.objects.all():
            res.append(faq)
            res.sort(key=lambda x: x.posted_on, reverse=True)
        context = {
            'active_tab':'faqs',
            'faqs':res,
        }
        return render(request,'admin-faqs.html',context)
    return redirect('/signin/')

def posts(request):
    if request.user.is_staff:
        res = []
        for post in Post.objects.all():
            ele ={'author':post.author.name,'time':post.datetime,
            'authorURL':reverse('account',args=[post.author.user.username]),
            'report':post.reports.all().count(),
            'url':'/post-detail/'+ str(post.id),'likes':post.likes.all().count(),'id':post.id, 'comments':post.comments.all().count()}
            res.append(ele)
        res.sort(key=lambda x: x.get('time'), reverse=True)
        res.sort(key=lambda x: x.get('report'), reverse=True)
        context = {
            'active_tab':'posts',
            'posts':res,
        }
        return render(request,'admin-posts.html',context)
    return redirect('/signin/')

def groups(request):
    if request.user.is_staff:
        res = []
        for group in Group.objects.all():
            ele={'title':group.title,'subtitle':str(group.member_count)+' members',
            'img':'','url':reverse('groups:group',args=[group.id]),'id':group.id, 'description':group.description}
            ele['joined']=request.user.account in group.members.all()
            if group.cover_image:
                ele['img']=group.cover_image.url
            res.append(ele)
        print(res)
        context = {
            'active_tab':'groups',
            'groups':res,
        }
        return render(request,'admin-groups.html',context)
    return redirect('/signin/')

def delete_account(request,id):
    if request.user.is_staff:
        try:
            Account.objects.get(id=id).delete()
            return JsonResponse({"message":"deleted the account","status":200})
        except:
            return JsonResponse({"message":"unable to delete this account","status":400})
    return redirect('/signin/')

def delete_post(request,id):
    if request.user.is_staff:
        try:
            Post.objects.get(id=id).delete()
            return JsonResponse({"message":"deleted the post","status":200})
        except:
            return JsonResponse({"message":"unable to delete this post","status":200})
    return redirect('/signin/')

def delete_group(request,id):
    if request.user.is_staff:
        try:
            Group.objects.get(id=id).delete()
            return JsonResponse({"message":"deleted the group","status":200})
        except:
            return JsonResponse({"message":"unable to delete this group","status":200})
    return redirect('/signin/')

def delete_faq(request,id):
    if request.user.is_staff:
        faq = get_object_or_404(Question, id=id)
        faq.delete()
        return redirect('/admin/faqs/')
    return redirect('/signin/')

def delete_event(request,id):
    if request.user.is_staff:
        event = get_object_or_404(Event, id=id)
        event.delete()
        return redirect('/admin/events/')
    return redirect('/signin/')