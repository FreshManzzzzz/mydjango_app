from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Quertion, Choice

"""
class_based view

"""


class IndexView(generic.ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Quertion.objects.filter(pub_date__lte=timezone.now()).order_by(
            '-pub_date'
        )[:5]


class DetailView(generic.DetailView):
    model = Quertion
    template_name = 'myapp/detail.html'
    context_object_name = 'question'

    def get_queryset(self):
        return Quertion.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Quertion
    template_name = 'myapp/results.html'
    context_object_name = 'question'

    def get_queryset(self):
        return Quertion.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Quertion, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': 'you did not select a choice',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))


"""
function view
"""
# def index(request):
#     latest_question_list = Quertion.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'myapp/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Quertion, pk=question_id)
#     return render(request, 'myapp/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Quertion, pk=question_id)
#     return render(request, 'myapp/results.html', {'question': question})
#
#
# def vote(request, question_id):
#     question = get_object_or_404(Quertion, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'myapp/detail.html', {
#             'question': question,
#             'error_message': 'you did not select a choice',
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))
