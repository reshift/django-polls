from django.template import Library
from polls.models import Poll
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse

register = Library()

@register.simple_tag()
def get_poll():
  try:
    poll = Poll.publishable.latest()
  except:
    poll = None

  return poll
  
#@register.inclusion_tag('polls/poll.haml', takes_context=True)
@register.simple_tag(takes_context=True)
def render_poll(context):
  try:
    poll = Poll.publishable.latest()
  except:
    return ""
 
  request = context['request']
  ip = request.META.get('REMOTE_ADDR','0.0.0.0')

  if poll.can_vote(ip):
    return render_to_response('polls/form.haml', {'poll': poll}, context_instance=context)
  else:
    return render_to_response('polls/results.haml', {'poll': poll}, context_instance=context)

@register.simple_tag(takes_context=True)
def render_poll_ajax(context):
  try:
    poll = Poll.publishable.latest()
  except:
    return ""

  js =  "$('#poll').load('/polls/latest/', function(response, status, xhr) {\n" + \
        "\tform = $('#poll form')[0];\n" + \
        "\tif(form) {\n" + \
        "\t\tform = $(form);\n" + \
        "\t\tform.submit(function(event) {\n" + \
        "\t\t\t/* stop form from submitting normally */\n" + \
        "\t\t\tevent.preventDefault();\n"  + \
        "\t\t\t/* Send the data using post and put the results in a div */\n" + \
        "\t\t\t$.post( form.attr('action'), form.serialize(),\n" + \
        "\t\t\tfunction( data ) {\n" + \
        "\t\t\t\t$('#poll').empty().append(data);\n" + \
        "\t\t\t}\n" + \
        "\t\t\t);\n" + \
        "\t\t});\n" + \
        "\t}\n" + \
        "});"

  return js
