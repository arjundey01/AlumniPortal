from post.views import comment
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from rest_framework import serializers

from .forms import QuestionForm
from .models import Question

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

class QuestionSerializer(serializers.ModelSerializer):
    ans_count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    content = serializers.CharField()
    id = serializers.IntegerField()
    posted_on = serializers.DateTimeField(format="%d %b %Y")
    views = serializers.IntegerField()

    class Meta:
        model = Question
        fields = ['ans_count', 'author', 'content', 'posted_on', 'id', 'views']

    def get_author(self, obj):
        if obj.author:
            author={}
            author['name']=(' ').join([ x.capitalize() for x in obj.author.name.split()])
            author['profile_img']= obj.author.profile_img_url
            author['username']=obj.author.user.username
            return author
        else:
            return 'Anonymous'

    def get_ans_count(self, obj):
        return int(obj.ans_count)

# As datetime object by itself is not json serialisable a
# fall_back_converter is written to serialize datetime.datetime
# objects which is passed as a default parameter of json.dumps()
def fall_back_converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%d %B %Y")

def get_questions(user):
    questions=[]
    if user.is_authenticated:
        follow_questions = []
        following_users = list(user.account.following.all())
        following_users.append(user.account)
        for fuser in following_users:
            for question in fuser.questions.all():
                question_age = datetime.datetime.now()-question.posted_on
                question_age = question_age.total_seconds() / 3600
                if question_age<=24:
                    follow_questions.append(question)
        follow_questions.sort(key=lambda x: x.posted_on, reverse=True)
        general_questions=list(Question.objects.all())
        general_questions.sort(key=lambda x:x.rev_priority)
        questions=follow_questions[:]
        for question in general_questions:
            if question not in follow_questions:
                questions.append(question)
    return questions


def load_question(request, index):
    load_count=5
    index = int(index)

    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({'error':'Not Logged In'}),status=500)
    
    if request.method == "POST":
        print("Post request receieved!")
        questions = get_questions(request.user)
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
    