from post.views import comment
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .forms import QuestionForm

# Create your views here.
def index(request):
    return render(request, 'faq.html')

def create_question(request):
    if request.method == "POST":
        print(request.POST)

        # create a QuestionForm instance from POST data
        # question_form = QuestionForm(request.POST) 

        # if question_form.is_valid():
        #     # create a new Question using question_form and dont commit to database.
        #     new_question = question_form.save(commit=False)
        #     new_question.author = request.user.account
        #     new_question.save()
        #     return redirect('faq')
        # else:
        #     return HttpResponse("Error in Question Form!")
        return HttpResponse("Post Received :)")
    else:
        ####################################
        ####################################
        ### DURING DEPLOYMENT RETURN 404 ###
        ####################################
        ####################################
        return HttpResponse("no post  request")
