from urllib import response
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
from django.shortcuts import render
from django.template import loader
# Create your views here.

# def index(request):
#     response = HttpResponse()
#     response.write("<h1>Welcome</h1>")
#     response.write("This is the polls app")
#     return response

# def detail(request, question_id):
#     return HttpResponse("You're looking at question % ." % question_id)

# def results(request, question_id):
#     response = "You're looking at result of question %s ."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     response = "You're voting on question %s ."
#     return HttpResponse(response % question_id)

# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     content_object_name = 'latest_question_list'
#     def get_queryset(self):
#         return Question.objects.order_by('-pub_date')[:5]

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'

# class ResultView(generic.DetailView):
#     model = Question
#     template_name = 'polls/result.html'

# class VoteView(generic.DetailView):
#     model = Question
#     template_name = 'polls/vote.html'

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list' : latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question is not found")
    return render(request,  'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))