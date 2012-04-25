from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from polls.models import *
from django.views.decorators.cache import never_cache

@never_cache
def latest(request):
  try:
    poll = Poll.publishable.latest()
  except:
    return HttpResponse("No active poll found.")
  ip = request.META.get('REMOTE_ADDR','0.0.0.0')

  if poll.can_vote(ip):
    # TODO: make into reverse call
    return redirect('/polls/form/%s' % poll.id)
  else:
    return redirect(poll.get_absolute_url())
  
@never_cache
def form(request, id):
  form = "foo"
  poll = get_object_or_404(Poll, pk=id)
  ip = request.META.get('REMOTE_ADDR','0.0.0.0')
  
  if poll.can_vote(ip) == False:
    return redirect(poll.get_absolute_url())
    
  return render_to_response('polls/form.haml', locals(), context_instance=RequestContext(request))

@never_cache
def vote(request, id):
  poll = get_object_or_404(Poll, pk=id)
  ip = request.META.get('REMOTE_ADDR','0.0.0.0')

  # if we can vote, vote
  if poll.can_vote(ip) == True:
    poll.vote(ip, request.POST.get('choice','0'))

  # redirect to results page
  return redirect(poll.get_absolute_url())

@never_cache
def results(request, id):
  poll = get_object_or_404(Poll, pk=id)
  return render_to_response('polls/results.haml', locals(), context_instance=RequestContext(request))