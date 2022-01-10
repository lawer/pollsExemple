from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('add_question/', views.add_question, name='add_question'),
    path('<int:question_id>/update/', views.update_question, name='update_question'),
    path('<int:question_id>/remove/', views.remove_question, name='remove_question'),
]