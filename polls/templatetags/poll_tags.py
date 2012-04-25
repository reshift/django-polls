from django import template
from polls.models import Poll
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse

register = template.Library()

class GetPoll(template.Node):
  def handle_token(cls, parser, token):
    args = token.contents.split()

    # {% get_poll %}        
    if len(args) == 1:
      return cls()

    # {% get_poll as [var] %}        
    if len(args) == 3 and args[1] == 'as':
      return cls(object_expr = parser.compile_filter(args[2]))
    
  handle_token = classmethod(handle_token)

  def __init__(self, as_varname=None):
    self.as_varname = as_varname

  def render(self, context):
    try:
      poll = Poll.publishable.latest()
    except:
      poll = None
    
    if self.as_varname: # if user gives us a variable to return
      context[self.as_varname] = poll
      return ''
    else:
      return poll

@register.tag()
def get_poll(parser, token):
    '''
    Returns a poll object
    '''
    return GetPoll.handle_token(parser, token)
  
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

  js =  "document.write('<div id=\"poll-content\"></div>');\n" + \
        "$('#poll-content').load('" + reverse('PollLatest') + "', function(response, status, xhr) {\n" + \
        "\tform = $('#poll-content form')[0];\n" + \
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
