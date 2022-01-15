from groups.models import Group
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render ,redirect, get_object_or_404
from django.urls import reverse
import requests
from django.core.files.storage import FileSystemStorage
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic.detail import DetailView
from users.models import Account
from groups.models import Group
from time import sleep
# Create your views here.

def feed(request):
    groups = {}
    for group in Group.objects.all():
        groups[group.title]=group.id
    return render(request,'feed.html',{'postform': PostForm, 'tags':json.dumps(groups)})

def individualfeed(request,id):
    groups = {}
    return render(request,'feed.html',{'postform': PostForm, 'tags':json.dumps(groups),'id':id})

def create_post(request):
    if request.method=='POST':
        next = request.GET.get('next')
        postform=PostForm(request.POST)
        if postform.is_valid():
            post=postform.save(commit=False)
            post.author=request.user.account
            post.save()
            for tag in postform.cleaned_data.get('tags'):
                post.tags.add(tag)
            post.save()
            if next:
                return redirect(next)
            return redirect('home')
        else:
            return HttpResponse('form-inv')
    else:
        return HttpResponse('Invalid')

def post_details(request, pk):
    post=Post.objects.get(pk=pk)
    return render(request,'post_create.html',{'post':post})

class PostDetailView(DetailView):
    model=Post
    context_object_name='post'

def update_post(request, pk):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            obj=get_object_or_404(Post, pk=pk)
            obj.delete()
        return redirect('post:mypage')
    else:
        obj=get_object_or_404(Post, pk=pk)
        form=PostForm(instance=obj)
        context={}
        context['form']=form
        return render(request, 'alumni_response/post_update.html', context)


def delete_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post=get_object_or_404(Post,pk=request.POST.get('id'))
            if post.author!=request.user.account:
                return HttpResponse('forbidden', status=403)
            post.delete()
            return HttpResponse('success')
        return HttpResponse('badRequest', status=400)
    return HttpResponse('notLoggedIn',status=500)

import json
from urllib.parse import unquote
def upload_image_view(request):
    f=request.FILES['image']
    fs=FileSystemStorage()
    filename=str(f)
    fileurl='posts/'+ request.user.username + '/'
    filepath=fs.save(fileurl + filename,f)
    fileurl=unquote(fs.url(filepath))
    return JsonResponse({'success':1,'file':{'url':fileurl,'path':filepath}})

def upload_file_view(request):
    f=request.FILES['file']
    size=int(request.POST['size'])
    fs=FileSystemStorage()
    filename=str(f)
    fileurl='posts/'+ request.user.username + '/'
    filepath=fs.save(fileurl + filename,f)
    fileurl=unquote(fs.url(filepath))
    return JsonResponse({'success':1,'file':{'url':fileurl,"size":size,"name":str(f),"extension":fileurl.split('.')[-1], "path": filepath}})


import datetime
def get_feed(user,tagNames=[]):
    feed=[]
    tags=[]
    for tname in tagNames:
        tags.append(get_object_or_404(Group, title = tname))
    print(tags)
    if user.is_authenticated:
        follow_feed=[]
        following = list(user.account.following.all())
        following.append(user.account)
        for fuser in following:
            for post in fuser.posts.all():
                post_age = datetime.datetime.now()-post.datetime
                post_age = post_age.total_seconds() / 3600
                if post_age<=24:
                    if len(tags) and len(list(set(tags) & set(post.tags.all())))==0:
                        continue
                    follow_feed.append(post)
        follow_feed.sort(key=lambda x: x.datetime, reverse=True)
        general_feed=list(Post.objects.all())
        general_feed.sort(key=lambda x:x.rev_priority)
        feed=follow_feed[:]
        for post in general_feed:
            if post not in follow_feed:
                if len(tags) and len(list(set(tags) & set(post.tags.all())))==0:
                        continue
                feed.append(post)
    return feed


def like_post(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        if request.user.is_authenticated:
            post=Post.objects.get(pk=post_id)
            acc=request.user.account
            if acc in post.likes.all():
                post.likes.remove(acc)
                msg="unliked"
            else:
                post.likes.add(acc)
                msg="liked"
            post.save()
            return HttpResponse(msg,status=200)
        else:
            return HttpResponse("Not Logged in!", status=500)
    else:
        return HttpResponse("unsuccessful", status=500)


from rest_framework import serializers
import json

class PostSerializer(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    datetime=serializers.DateTimeField(format="%d %b,%Y %I:%M %p")
    class Meta:
        model = Post
        fields = ['author','like_count','datetime','content','id','comment_count']
    def get_author(self, post):
        if post.author:
            author={}
            author['name']=(' ').join([ x.capitalize() for x in post.author.name.split()])
            author['profile_img']= post.author.profile_img_url
            author['username']=post.author.user.username
            author['desg']=post.author.designation.title + " | " + post.author.organization.name
            return author
        else:
            return 'Anonymous'
    def get_like_count(self,post):
        return len(post.likes.all())
    def get_comment_count(self,post):
        return len(post.comments.all())
    def get_id(self,post):
        return post.pk






def load_feed(request,index):
    load_count=5
    index=int(index)
    user=request.user
    if not user.is_authenticated:
        return HttpResponse(json.dumps({'error':'Not Logged In'}),status=500)
    tags=[]
    if request.method == 'POST':
        tags = json.loads(request.POST.get('tags'))

    feed=get_feed(user,tags)
    posts=[]
    if len(feed)>index*load_count:
        for post in feed[index*load_count:min(len(feed),load_count*(index+1))]:
            print(post.content)
            data=PostSerializer(post).data
            data['is_liked']=user.account in post.likes.all()
            posts.append(data)
        return HttpResponse(json.dumps(posts),status=200)
    else:
        return HttpResponse(json.dumps({'error':'No more posts'}),status=500)

def individual_post(request,id):
    id=int(id)
    user=request.user
    if not user.is_authenticated:
        return HttpResponse(json.dumps({'error':'Not Logged In'}),status=500)
    posts=[]
    post = Post.objects.get(id=id)
    data=PostSerializer(post).data
    data['is_liked']=user.account in post.likes.all()
    posts.append(data)
    return HttpResponse(json.dumps(posts),status=200)



def comment(request, pk):
    if request.method=='POST':
        commentform=CommentForm(request.POST)
        post=get_object_or_404(Post, pk=pk)
        if commentform.is_valid():
            comment=commentform.save(commit=False)
            comment.post=post
            comment.author=request.user.account
            comment.save()
            return HttpResponse('success')
            # return HttpResponse(json.dumps(comment), status=200)
        else:
            return HttpResponse('form-inv', status=500)
    else:
        return HttpResponse('Invalid', status=500)


def load_comment(request, id):
  
    # comments=Comment.objects.all().filter(pk=id)
    comments=[]
    for comment in Post.objects.get(pk=id).comments.all():
        dic={}
        dic['author']=comment.author.name
        dic['profile_img']=comment.author.profile_img_url
        dic['create_date']=comment.create_date.strftime("%d/%m/%y")
        dic['content']=comment.content
        comments.append(dic)
    print(comments)
    return HttpResponse(json.dumps(comments), status=200)


def load_likes(request, id):
    likes=[]
    for like in get_object_or_404(Post, pk=id).likes.all():
        dic={}
        dic['author']=like.name
        dic['username']=like.user.username
        dic['profile_img']=like.profile_img_url
        likes.append(dic)
    return HttpResponse(json.dumps(likes), status=200)