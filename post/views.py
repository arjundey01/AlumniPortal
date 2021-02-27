from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render ,redirect, get_object_or_404
from django.urls import reverse
import requests
from django.core.files.storage import FileSystemStorage
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic.detail import DetailView
from users.models import Account
# Create your views here.

def index(request):
    return render(request,'post_create.html',{'postform':PostForm})
def create_post(request):
    if request.method=='POST':
        postform=PostForm(request.POST)
        print(request.POST)
        if postform.is_valid():
            post=postform.save(commit=False)
            post.author=request.user.account
            post.save()
            return redirect('post:feed')
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


def delete_post(request,pk):
    if request.user.is_authenticated:
        try:
            post=Post.objects.get(pk=pk)
            post.delete()
            return HttpResponse('success')
        except Post.DoesNotExist:
            return HttpResponse('doesNotExist',status=500)
    else:
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

def feign_image_upload(request):
    resp=upload_image_view(request)
    fs=FileSystemStorage()
    filename=json.loads(resp.content)['file']['path']
    print(filename)
    fs.delete(filename)
    return resp

def upload_file_view(request):
    f=request.FILES['file']
    size=int(request.POST['size'])
    fs=FileSystemStorage()
    filename=str(f)
    fileurl='posts/'+ request.user.username + '/'
    filepath=fs.save(fileurl + filename,f)
    fileurl=unquote(fs.url(filepath))
    return JsonResponse({'success':1,'file':{'url':fileurl,"size":size,"name":str(f),"extension":"ext", "path": filepath}})
    # return redirect('alumni_response:mypage')

def feign_file_upload(request):
    resp=upload_file_view(request)
    fs=FileSystemStorage()
    filename=json.loads(resp.content)['file']['path']
    fs.delete(filename)
    return resp
# class PostDetailView(DetailView):
#     model=Post
#     context_object_name='post'
import datetime
def get_feed(user):
    feed=[]
    if user.is_authenticated:
        follow_feed=[]
        following = list(user.account.following.all())
        following.append(user.account)
        for fuser in following:
            for post in fuser.posts.all():
                post_age = datetime.datetime.now()-post.datetime
                post_age = post_age.total_seconds() / 3600;
                if post_age<=24:
                    follow_feed.append(post)
        follow_feed.sort(key=lambda x: x.datetime, reverse=True)
        general_feed=list(Post.objects.all())
        general_feed.sort(key=lambda x:x.rev_priority)
        feed=follow_feed[:]
        for post in general_feed:
            if post not in follow_feed:
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
    datetime=serializers.DateTimeField(format="%d %b,%Y %H:%M:%S")
    class Meta:
        model = Post
        fields = ['author','like_count','datetime','content','id']
    def get_author(self, post):
        if post.author:
            return (' ').join([ x.capitalize() for x in post.author.name.split()])
        else:
            return 'Anonymous'
    def get_like_count(self,post):
        return len(post.likes.all())
    def get_id(self,post):
        return post.pk




def load_feed(request,index):
    load_count=5
    index=int(index)
    user=request.user
    if not user.is_authenticated:
        return HttpResponse(json.dumps({'error':'Not Logged In'}),status=500)
    feed=get_feed(user)
    posts=[]
    if len(feed)>=index*load_count:
        for post in feed[index*load_count:min(len(feed),load_count*(index+1))]:
            data=PostSerializer(post).data
            data['is_liked']=user.account in post.likes.all()
            posts.append(data)
        return HttpResponse(json.dumps(posts),status=200)
    else:
        return HttpResponse(json.dumps({'error':'No more posts'}),status=500)

def feed(request):
    return render(request, 'feed.html')