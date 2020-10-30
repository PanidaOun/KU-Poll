"""View for application polls."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Choice, Question
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from polls.models import Vote

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import logging.config

from .settings import LOGGING



logging.config.dictConfig(LOGGING)
loggings = logging.getLogger("polls")

def get_client_ip(request):
    """ Get the client's ip"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def logging_log_in(sender, request, user, **kwargs):
    loggings.info(f"{user.username} is login to KU POLL, {user.username}'s IP address is {get_client_ip(request)}")

@receiver(user_logged_out)
def logging_logged_out(sender, request, user, **kwargs):
    loggings.info(f"{user.username} is logout from KU POLL, {user.username}'s IP address is {get_client_ip(request)}")

@receiver(user_login_failed)
def logging_failed_logged_in(sender, request, credentials, **kwargs):
    loggings.warning(f"{request.POST['username']} failed to login to KU POLL, {request.POST['username']}'s IP address is {get_client_ip(request)}")

class IndexView(generic.ListView):
    """Class to view a index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
@login_required
def view_vote(request, question_id):
    """Return to index page if user cannot vote the question but if user can vote ,go to detail page."""
    question = get_object_or_404(Question, pk=question_id)
    user=request.user
    previous_vote = False
    previous_vote_text = ""
    if not question.can_vote():
        messages.error(request, "Voting is not allowed")
        return redirect('polls:index')
    if Vote.objects.filter(user=user,question=question):
        previous_vote_text = Vote.objects.filter(user=user,question=question).first().choice.choice_text
        previous_vote = True
        return render(request, 'polls/detail.html', {'question': question,'previous_vote_text':previous_vote_text,'previous_vote':previous_vote})
    return render(request, 'polls/detail.html', {'question': question})



class ResultsView(generic.DetailView):
    """Class to view a result page."""

    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """Def about vote and go to result page."""
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Vote.objects.update_or_create(user = user, question=question, defaults={'choice': selected_choice})
        
        loggings.info(f"{user.username} is voting in question id {question_id}, {user.username}'s IP address is {get_client_ip(request)}")    

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
