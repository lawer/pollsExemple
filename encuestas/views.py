from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions

from encuestas.models import Question, Choice
from encuestas.serializers import UserSerializer, QuestionSerializer, ChoiceSerializer


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
    question = Question.objects.get(pk=question_id)
    return render(request, 'encuestas/results.html', {
        "question": question
    })


def vote(request, question_id):
    question = Question.objects.get(pk=question_id)
    choice_id = int(request.POST["choice"])

    choice = question.choice_set.get(pk=choice_id)
    choice.votes += 1

    choice.save()

    return redirect(
        to='results',
        question_id=question_id
    )


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'mood']


@login_required
def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()

            return redirect(to="index")
    else:
        form = QuestionForm()
    return render(request, 'encuestas/add_question.html', {
        "form": form
    })


@login_required
def update_question(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=q)

        if form.is_valid():
            form.save()
            messages.success(request, 'Pregunta actualizada.')
            return redirect(to="index")
    else:
        form = QuestionForm(instance=q)
    return render(request, 'encuestas/add_question.html', {
        "form": form
    })


def remove_question(request, question_id):
    question = Question.objects.get(pk=question_id)

    if request.method == "POST":
        question.delete()
        return redirect(to="index")

    return render(request, 'encuestas/remove_question.html', {
        "question": question
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
