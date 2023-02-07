from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice, User
import pdb
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
# Get questions and display them


def login_view(request):
    if request.method == "POST":
       
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("polls:index"))
        else:
            return render(request, "polls/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "polls/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("polls:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "polls/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "polls/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("polls:index"))
    else:
        return render(request, "polls/register.html")



def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')
    #paginator = Paginator(latest_question_list, 5)
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html',context)

# Show specific question and choices


def detail(request, question_id):
	try:
		question = Question.objects.get(pk = question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question': question})

#Get question and display results


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    poll_results=[]
    allchoices=Choice.objects.all().filter(question=question)
    for choice in allchoices:
        votes=choice.votes
        poll_results.append([choice.choice_text,votes])
    return render(request, 'polls/results.html', context={'question': question, "poll_results":poll_results})
	


def vote(request, question_id):
        question = get_object_or_404(Question, pk = question_id)

        poll_results = []
        try:
            selected_choice = question.choice_set.get(pk = request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))