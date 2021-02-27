from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from .graph_helper import get_user
from .models import Account, Contact
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
import json


def home(request):
    context = initialize_context(request)

    return render(request, 'home.html', context)


def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    #context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)


def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)
    # Get the user's profile
    user = get_user(token)
    is_signup = False
    if not User.objects.filter(username=user['mail']).exists():
        is_signup = True
        new_user = User.objects.create_user(user['mail'])
        new_user.save()
        account = Account()
        account.user = new_user
        account.name = user['displayName']
        account.email = user['mail']
        account.save()
    login(request, User.objects.get(username=user['mail']))
    store_token(request, token)
    #store_user(request, user)
    # if is_signup:
    #     return redirect('signup-details')
    #else:
    return HttpResponseRedirect(reverse('home'))

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


def profile(request, username):
    user=get_object_or_404(User, username=username).account
    experiences=Experience.objects.all().filter(user=user)
    projects=Project.objects.all().filter(user=user)
    educations=Education.objects.all().filter(user=user)
    # contact=get_object_or_404(Contact, user=request.user)
    context ={
            'curr_user': user,
            'experiences':experiences,
            'projects' :projects,
            'educations': educations,
        }
    if(request.user == user.user):
        context['u_form']=UserUpdateForm(instance=request.user)
        context['e_form']=ExperienceForm()
        context['edu_form']=EducationForm()
        context['p_form']=ProjectForm()
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
def experience(request):
    if request.method == 'POST':
        e_form=ExperienceForm(request.POST)
        if e_form.is_valid():
            e=e_form.save(commit=False)
            e.user=request.user.account
            e.save()
            messages.success(request, 'Your Experience has been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
    return redirect('/account/'+request.user.username+'#tab-experience')

@login_required(login_url='/signin/')
def project(request):
    if request.method == 'POST':
        p_form=ProjectForm(request.POST)
        if p_form.is_valid():
            p=p_form.save(commit=False)
            p.user=request.user.account
            p.save()
            messages.success(request, 'Your Projects have been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
    return redirect('/account/'+request.user.username+'#tab-project')

@login_required(login_url='/signin/')
def education(request):
    if request.method == 'POST':
        edu_form=EducationForm(request.POST)
        if edu_form.is_valid():
            edu=edu_form.save(commit=False)
            edu.user=request.user.account
            edu.save()
            messages.success(request, 'Your Education has been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
        return redirect('/account/'+request.user.username+'#tab-education')


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
def update_ex(request, pk):
    if request.method == 'POST':
        e_form=ExperienceForm(request.POST, instance=get_object_or_404(Experience, pk=pk))
        if e_form.is_valid():

            e=e_form.save(commit=False)
            e.user=request.user.account
            e.save()
            messages.success(request, 'Your experience has been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
        return redirect('/account/'+request.user.username+'#tab-experience')
    return Http404


@login_required(login_url='/signin/')
def update_p(request, pk):
    if request.method == 'POST':
        p_form=ProjectForm(request.POST, instance=get_object_or_404(Project, pk=pk))
        if p_form.is_valid():

            p=p_form.save(commit=False)
            p.user=request.user.account
            p.save()
            messages.success(request, 'Your project has been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
        return redirect('/account/'+request.user.username+'#tab-projects')
    return Http404

@login_required(login_url='/signin/')
def update_edu(request, pk):
    if request.method == 'POST':
        edu_form=EducationForm(request.POST, instance=get_object_or_404(Education, pk=pk))
        if edu_form.is_valid():

            edu=edu_form.save(commit=False)
            edu.user=request.user.account
            edu.save()
            messages.success(request, 'Your education has been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
        return redirect('/account/'+request.user.username+'#tab-education')
    return Http404

@login_required(login_url='/signin/')
def update_photo(request):
    if request.method == 'POST':
        photo_form=SignupForm(request.POST, instance=get_object_or_404(Account, user=request.user))
        if photo_form.is_valid():

            photo=photo_form.save(commit=False)
            photo.save()
            messages.success(request, 'Your profile image has been Updated!')
        else:
            messages.error(request,"Some Error Occured!")
        return redirect('/account/')
    return Http404

@login_required(login_url='/signin/')
def delete_item(request,type,pk):
    if type == 'experience':
        exp = get_object_or_404(Experience, pk=pk)
        exp.delete()
    elif type == 'project':
        proj = get_object_or_404(Project, pk=pk)
        proj.delete()
    elif type == 'education':
        edu = get_object_or_404(Education, pk=pk)
        edu.delete()
    messages.success(request, 'The entry has been Deleted!')

    return redirect('/account/'+request.user.username+'#tab-'+type)
    