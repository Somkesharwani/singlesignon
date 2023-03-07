import json

from . import models
from .models import Poll, Answer
from polls.forms.user import ProfileForm
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


@login_required
def index(request):
    polls = Poll.objects.all()
    poll_list = []
    for poll in polls:
        answers = poll.answers.all()
        answer_list = []
        for answer in answers:
            answer_list.append({
                "value": answer.value,
                "user_first_name": answer.user.first_name,
                "user_last_name": answer.user.last_name,
                "id": answer.pk,
            })
        poll_list.append({
            "title": poll.title,
            "id": poll.pk,
            "answers": answer_list
        })
    context = {'polls': poll_list}
    return render(request, 'polls/index.html', context)


@login_required
def my_profile(request):
    profile = request.user.profile
    try:
        user_form = models.ProfileForm.objects.get(site=profile.site)
        fields = user_form.form_fields['fields']
        data = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        }
        data.update(profile.dynamic_fields)
        form = ProfileForm(fields=fields, initial=data)
        return render(request, 'polls/current_user.html', {'form': form})
    except:
        return Http404("ProfileForm doesn't exist") 


@login_required
@csrf_exempt
def edit_answer(request, poll_id, answer_id):
    payload = json.loads(request.body)
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.value = payload.get('value')
    answer.save()
    return JsonResponse({"value": answer.value})


@login_required
def answer(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == "POST":
        ans = request.POST.get('your_answer')
        answer = Answer.objects.create(poll=poll, user=request.user, value=ans)
        answer.save()
        return redirect('polls:index')
    elif request.method == "GET":
        answers = poll.answers.only('value')
        context = {"poll": poll, "answers": answers}
        return render(request,'polls/answer.html',context)

@login_required
def question(request):
    if request.method == "POST":
        quest = Poll.objects.create(title=request.POST.get('your_quest'))
        quest.save()
        return redirect("polls:index")
    elif request.method == "GET":
        lst = Poll.objects.all()
        context = { 'latest_question_list': lst, }
        return render(request=request,template_name='polls/question.html',context=context)

@login_required
def question_form(request):
    return render(request=request,template_name='polls/add_question.html')

@login_required
def answer_form(request,poll_id):
    question =get_object_or_404(Poll,pk=poll_id)
    context = { 
        'poll_id':poll_id,
        'question':question
        }
    return render(request=request,template_name='polls/add_answer.html',context=context)

