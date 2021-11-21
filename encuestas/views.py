from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from encuestas.models import Question


def index(request):
    questions = Question.objects.all().order_by("pub_date")[:5]

    return render(request, "encuestas/index.html", {
        "ultimas_preguntas": questions
    })


def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, "encuestas/detail.html", {
        "question": question
    })


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
