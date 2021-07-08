from datetime import date
from json.encoder import JSONEncoder
import re
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse
from .auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from .graph_helper import get_user
from .models import Account, Contact, Institute
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from post.views import feed
from groups.models import Group
from .forms import *
import json
import operator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from fuzzywuzzy import fuzz

def home(request):
    if request.user.is_authenticated:
        return feed(request)
    return render(request, 'home.html')


def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)

@login_required(login_url='/signin/')
def details(request):
    context={'user':request.user}
    context['u_form']=UserUpdateForm(instance=request.user)
    context['e_form']=ExperienceForm()
    context['j_form']=PastJobsForm()
    context['pro_form']=profileForm
    print(request)
    return render(request, 'details.html',context)

def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)
    # Get the user's profile
    user = get_user(token)
    if not User.objects.filter(username=user['mail']).exists():
        new_user = User.objects.create_user(user['mail'])
        new_user.save()
        account = Account()
        account.user = new_user
        account.name = user['displayName']
        account.email = user['mail']
        account.save()
        return HttpResponseRedirect(reverse('details'))
    login(request, User.objects.get(username=user['mail']))
    store_token(request, token)
    return HttpResponseRedirect(reverse('home'))
def updateProfile(request):
    pro_form=profileForm(request.POST or None, instance=get_object_or_404(Account,user=request.user))

    if pro_form.is_valid():
        p=pro_form.save(commit=False)
        if operator.contains(p.email ,"alumni"):
            p.is_alumni=True
        p.save()
        messages.success(request, 'Your information has been Updated!')
        return JsonResponse({'succes':'saved'})
    else:
         return HttpResponseBadRequest
    
def signup_details(request):
    if request.user.is_authenticated:
        context={}
        context['signup-form']=SignupForm()
        return render(request,'signup-details.html',context)
    else:
        return HttpResponse('notLoggedIn',status=500)
            
def update_details(request):
    pass

def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)
    logout(request)
    return HttpResponseRedirect(reverse('home'))

# def test_signup(request,name,email):
#     if list(filter(lambda x:x.email==email,User.objects.all()))==[]:
#       new_user=User()
#       new_user.name=name
#       new_user.email=email
#       new_user.save();
#       return HttpResponseRedirect(reverse('home'))
#     else:
#       return HttpResponse('exists')

def test_signin(request, name):
    user = Account.objects.get(name=name).user
    login(request, user)
    return HttpResponseRedirect(reverse('home'))

def follow(request):
    if request.user.is_authenticated:
        user = request.user.account
        username=request.GET.get("username")
        try:
            tofollow = User.objects.get(username=username).account
            user.following.add(tofollow)
            user.save()
            return HttpResponse('success',status=200)
        except User.DoesNotExist:
            return HttpResponse('doesnotexist',status=404)
    return HttpResponse('notloggedin',status=500)

def unfollow(request):
    if request.user.is_authenticated:
        user = request.user.account
        username=request.GET.get("username")
        try:
            toUnfollow = User.objects.get(username=username).account
            user.following.remove(toUnfollow)
            user.save()
            res = user.following.all()
            return HttpResponse('success',status=200)
        except User.DoesNotExist:
            return HttpResponse('doesnotexist',status=500)
    return HttpResponse('notloggedin',status=500)

def followers(request):
    if request.user.is_authenticated:
        user = request.user.account
        return HttpResponse(json.dumps([x.name for x in user.followers.all()]))
    return HttpResponse('notloggedin')

def following(request):
    if request.user.is_authenticated:
        user = request.user.account
        return HttpResponse(json.dumps([x.name for x in user.following.all()]))
    return HttpResponse('notloggedin')

def account(request):
    context={}
    context['user']=User.objects.get(username="arjundey@iitg.ac.in")
    return render(request,'profile.html',context)




#========================================== PROFILE ==================================================

def profile(request, username):
    user=get_object_or_404(User, username=username).account
    experiences=Experience.objects.all().filter(user=user)
    projects=Project.objects.all().filter(user=user)
    educations=Education.objects.all().filter(user=user)
    jobs=PastJobs.objects.all().filter(user=user)
    # contact=get_object_or_404(Contact, user=request.user)
    context ={
            'curr_user': user,
            'experiences':experiences,
            'projects' :projects,
            'educations': educations,
            'jobs':jobs
        }
    if(request.user == user.user):
        if Contact.objects.filter(user=user).exists():
            context['ct_form']=ContactUpdateForm(instance=user.contact)
        else:
            context['ct_form']=ContactUpdateForm()

    return render(request, 'profile.html', context)

@login_required(login_url='/signin/')
def update_account(request):
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid() :
            u_form.save()
            messages.success(request, 'Your Account has been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
        return redirect('/account/'+request.user.username+'#tab-update')
    return Http404

@login_required(login_url='/signin/')
def experience(request, action):
    if action == 'delete':
        return delete_item(request, 'experience')
    if request.method == 'POST':
        try:
            if action == 'add':
                exp = Experience()
                exp.user = request.user.account
            else:
                exp = get_object_or_404(Experience, pk=request.POST.get('pk'))
            if request.POST.get('start_date')!='':
                exp.start_date=request.POST.get('start_date')
            if request.POST.get('end_date')!='':
                exp.end_date=request.POST.get('end_date')
            exp.description=request.POST.get('description')
            exp.experience=request.POST.get('experience')
            exp.organization, created =Organization.objects.get_or_create(name=request.POST.get('organization'))
            exp.save()
            return redirect('/account/'+request.user.username)
        except:
            return HttpResponseBadRequest()  
    return HttpResponseBadRequest()

@login_required(login_url='/signin/')
def pastjobs(request, action):
    if action == 'delete':
        return delete_item(request, 'job')
    if request.method == 'POST':
        try:
            if action == 'add':
                job = PastJobs()
                job.user = request.user.account
            else:
                job = get_object_or_404(PastJobs, pk=request.POST.get('pk'))
            if request.POST.get('start_date')!='':
                job.start_date=request.POST.get('start_date')
            if request.POST.get('end_date')!='':
                job.end_date=request.POST.get('end_date')
            job.description=request.POST.get('description')
            job.organization, created =Organization.objects.get_or_create(name=request.POST.get('organization'))
            job.designation, created=Designation.objects.get_or_create(title=request.POST.get('designation'))
            job.save()
            return redirect('/account/'+request.user.username)
        except:
            return HttpResponseBadRequest()  
    return HttpResponseBadRequest()

@login_required(login_url='/signin/')
def project(request, action):
    if action == 'delete':
        return delete_item(request, 'project')
    if request.method == 'POST':
        try:
            if action == 'add':
                project = Project()
                project.user = request.user.account
            else:
                project = get_object_or_404(Project, pk=request.POST.get('pk'))
            if request.POST.get('start_date')!='':
                project.start_date=request.POST.get('start_date')
            if request.POST.get('end_date')!='':
                project.end_date=request.POST.get('end_date')
            project.description=request.POST.get('description')
            project.project=request.POST.get('project')
            project.save()
            return redirect('/account/'+request.user.username)
        except:
            return HttpResponseBadRequest()  
    return HttpResponseBadRequest()

@login_required(login_url='/signin/')
def education(request, action):
    if action == 'delete':
        return delete_item(request, 'education')
    if request.method == 'POST':
        try:
            if action == 'add':
                edu = Education()
                edu.user = request.user.account
            else:
                edu = get_object_or_404(Education, pk=request.POST.get('pk'))
            if request.POST.get('start_date')!='':
                edu.start_date=request.POST.get('start_date')
            if request.POST.get('end_date')!='':
                edu.end_date=request.POST.get('end_date')
            edu.description=request.POST.get('description')
            edu.education=request.POST.get('education')
            edu.institute, created =Institute.objects.get_or_create(name=request.POST.get('institute'))
            edu.save()
            return redirect('/account/'+request.user.username)
        except:
            return HttpResponseBadRequest()  
    return HttpResponseBadRequest()

@login_required(login_url='/signin/')
def update_contact(request):
    if request.method == 'POST':
        if Contact.objects.filter(user=request.user.account).exists():
            ct_form=ContactUpdateForm(request.POST, instance=request.user.account.contact)
        else:
            ct_form=ContactUpdateForm(request.POST)
        if ct_form.is_valid():

            contact=ct_form.save(commit=False)
            contact.user=request.user.account
            contact.save()
            messages.success(request, 'Your Contact has been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
        return redirect('/account/'+request.user.username+'#tab-contact')
    return Http404

@login_required(login_url='/signin/')
def update_photo(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.account.profile_img = form.cleaned_data.get('image')
            request.user.account.save()
            return redirect('/account/'+request.user.username)
    return HttpResponseBadRequest()


def delete_item(request, type):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method=='POST':
        pk = request.POST.get('pk')
        if type == 'experience':
            exp = get_object_or_404(Experience, pk=pk)
            if exp.user != request.user.account:
                return HttpResponseForbidden()
            exp.delete()
        elif type == 'project':
            proj = get_object_or_404(Project, pk=pk)
            if proj.user != request.user.account:
                return HttpResponseForbidden()
            proj.delete()
        elif type == 'education':
            edu = get_object_or_404(Education, pk=pk)
            if edu.user != request.user.account:
                return HttpResponseForbidden()
            edu.delete()
        elif type=='job':
            job = get_object_or_404(PastJobs, pk=pk)
            if job.user != request.user.account:
                return HttpResponseForbidden()
            job.delete()
        return HttpResponse('success',status=200)
    return HttpResponseBadRequest()



def search(query, user):
    res = {'group':[],'alumni':[],'student':[]}
    for group in Group.objects.all():
        score = fuzz.partial_ratio(query, group.title)
        if score>50:
            ele={'title':group.title,'subtitle':str(group.member_count)+' members',
            'img':group.cover_image.url,'url':reverse('groups:group',args=[group.id]),'id':group.id,'match':score}
            ele['joined']=user.account in group.members.all()
            res['group'].append(ele)
    for acc in Account.objects.all():
        if acc == user.account:
            continue
        score = fuzz.partial_ratio(query, acc.name)
        cat = 'alumni' if acc.is_alumni else 'student'
        if score>50:
            ele ={'title':acc.name,'subtitle':acc.designation.title,'img':acc.profile_img_url,
            'url':reverse('account',args=[acc.user.username]),'username':acc.user.username,'match':score}
            ele['followed']=user.account in acc.followers.all()
            res[cat].append(ele)
    res['group'].sort(key=lambda x:x.get('match'))
    res['alumni'].sort(key=lambda x:x.get('match'))
    res['student'].sort(key=lambda x:x.get('match'))
    return res

def search_sugg(request):
    query = request.GET.get('query')
    res = search(query, request.user)        
    return HttpResponse(json.dumps({'query':query,'results':res}))


def search_res(request):
    query = request.GET.get('query')
    res = search(query, request.user)
    return render(request, "search_results.html",{"results":res})

@login_required
def suggestions(request):
    res = []
    for acc in Account.objects.all():
        if acc in request.user.account.following.all() or acc==request.user.account:
            continue
        score=0
        score+=len(list(set(acc.groups.all()) & set(request.user.account.groups.all())))/len(Group.objects.all())
        score+=int(acc.organization == request.user.account.organization)
        ele ={'title':acc.name,'subtitle':acc.designation.title,'img':acc.profile_img_url,
            'url':reverse('account',args=[acc.user.username]),'username':acc.user.username,'score':score}
        res.append(ele)
    res.sort(key=lambda x:x.get('score'))
    return HttpResponse(json.dumps(res))
    
