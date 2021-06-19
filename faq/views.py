from groups.models import Group
from post.views import comment
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import serializers

from .forms import QuestionForm, AnswerForm
from .models import Answer, Question
from groups.models import Group

import json, datetime

# Create your views here.
def index(request):
    return render(request, 'faq.html')

def create_question(request):
    if request.method == "POST":
        # create a QuestionForm instance from POST data
        question_form = QuestionForm(request.POST) 

        if question_form.is_valid():
            # create a new Question using question_form and dont commit to database.
            new_question = question_form.save(commit=False)
            new_question.author = request.user.account
            new_question.save()
            return redirect('faq')
        else:
            ##################################################
            ##################################################
            ### DURING DEPLOYMENT RETURN CUSTOM ERROR PAGE ###
            ##################################################
            ##################################################
            return HttpResponse("Error in Question Form!")
    else:
        ####################################
        ####################################
        ### DURING DEPLOYMENT RETURN 404 ###
        ####################################
        ####################################
        return HttpResponse("No Post Request")

def create_answer(request, id):
    if request.method == "POST":
        ans_form = AnswerForm(request.POST)
        if ans_form.is_valid():
            new_ans = ans_form.save(commit=False)
            new_ans.author = request.user.account
            new_ans.question = get_object_or_404(Question, pk=id)
            new_ans.save()
            return redirect('faq:detail_question', id=id)
        else:
            ##################################################
            ##################################################
            ### DURING DEPLOYMENT RETURN CUSTOM ERROR PAGE ###
            ##################################################
            ##################################################
            print(ans_form.errors)
            return HttpResponse("Error in Answer Form!")
    else:
        ####################################
        ####################################
        ### DURING DEPLOYMENT RETURN 404 ###
        ####################################
        ####################################
        return HttpResponse("No Post Request")

def question_detail(request, id):
    question = get_object_or_404(Question, pk = id)
    answers = list(question.answers.all())
    answers.sort(key=lambda x: x.posted_on, reverse=True)
    answers.sort(key=lambda x: x.rev_priority)
    context = {
        'question': question,
        'answers': answers,
    }
    return render(request, 'question_detail.html', context);

class QuestionSerializer(serializers.ModelSerializer):
    ans_count = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    posted_on = serializers.DateTimeField(format="%d %b %Y")

    class Meta:
        model = Question
        fields = ['ans_count', 'answers', 'author', 'content', 'posted_on', 'id', 'views']

    def get_ans_count(self, obj):
        return int(obj.ans_count)
    
    def get_answers(self, obj):
        all_answers = list(obj.answers.all())
        all_answers.sort(key=lambda x: x.posted_on, reverse=True)
        all_answers.sort(key=lambda x: x.rev_priority)
        answer = {}
        if len(all_answers):
            answer['name'] = all_answers[0].author.name
            answer['profile_img'] = all_answers[0].author.profile_img_url
            answer['content'] = all_answers[0].content
        return answer

    def get_author(self, obj):
        if obj.author:
            author={}
            author['name']=(' ').join([ x.capitalize() for x in obj.author.name.split()])
            author['profile_img']= obj.author.profile_img_url
            author['username']=obj.author.user.username
            return author
        else:
            return 'Anonymous'

def get_questions(user, tagNames = []):
    questions=[]
    tags = []
    for tag in tagNames:
        tags.append(get_object_or_404(Group, title = tag))

    if user.is_authenticated:
        follow_questions = []
        following_users = list(user.account.following.all())
        following_users.append(user.account)
        for fuser in following_users:
            for question in fuser.questions.all():
                question_age = datetime.datetime.now()-question.posted_on
                question_age = question_age.total_seconds() / 3600
                if question_age<=24:
                    if len(tags) and len(list( set (tags) & set (question.tags.all()) )) == 0:
                        continue
                    follow_questions.append(question)
        follow_questions.sort(key=lambda x: x.posted_on, reverse=True)
        general_questions=list(Question.objects.all())
        general_questions.sort(key=lambda x:x.rev_priority)
        questions = follow_questions[:]
        for question in general_questions:
            if len(tags) and len(list( set (tags) & set (question.tags.all()) )) == 0:
                continue
            if question not in follow_questions:
                questions.append(question)
    return questions

def load_question(request, index):
    load_count=5
    index = int(index)

    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({'error':'Not Logged In'}),status=500)

    tags = []
    if request.method == "POST":
        tags = json.loads(request.POST.get('tags'))
        questions = get_questions(request.user, tags)
        questions_to_be_sent=[]
        if len(questions) > index*load_count:
            for question in questions[index*load_count:min(len(questions),load_count*(index+1))]:
                data = QuestionSerializer(question).data
                questions_to_be_sent.append(data)
            return HttpResponse(json.dumps(questions_to_be_sent),status=200)
        else:
            return HttpResponse(json.dumps({'error':'No more posts'}),status=500)

    ##################################################
    ##################################################
    ### DURING DEPLOYMENT RETURN CUSTOM ERROR PAGE ###
    ##################################################
    ##################################################
    return HttpResponse("You aren't suppose to see this!")
    
def get_best4(request):
    questions=[]
    tags = []
    for tag in tagNames:
        tags.append(get_object_or_404(Group, title = tag))

    if user.is_authenticated:
        follow_questions = []
        following_users = list(user.account.following.all())
        following_users.append(user.account)
        for fuser in following_users:
            for question in fuser.questions.all():
                question_age = datetime.datetime.now()-question.posted_on
                question_age = question_age.total_seconds() / 3600
                if question_age<=24:
                    if len(tags) and len(list( set (tags) & set (question.tags.all()) )) == 0:
                        continue
                    follow_questions.append(question)
        follow_questions.sort(key=lambda x: x.posted_on, reverse=True)
        general_questions=list(Question.objects.all())
        general_questions.sort(key=lambda x:x.rev_priority)
        questions = follow_questions[:]
        for question in general_questions:
            if len(tags) and len(list( set (tags) & set (question.tags.all()) )) == 0:
                continue
            if question not in follow_questions:
                questions.append(question)
    return questions