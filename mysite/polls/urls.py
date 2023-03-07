from django.urls import path
from django.views.generic.base import TemplateView

from polls import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('question', views.question, name='question'),
    path('myprofile', views.my_profile, name='my_profile'),
    path('<int:poll_id>/answers', views.answer, name='answer'),
    path('<int:poll_id>', views.answer_form, name='add_answer'),
    path('add_question', views.question_form, name='add_question'),
    path('<int:poll_id>/answers/<int:answer_id>/edit', views.edit_answer, name='edit_answer'),
]
