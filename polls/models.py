from django.db import models
from datetime import *

class ActivePollManager(models.Manager):
  def get_query_set(self):
    return super(ActivePollManager, self).get_query_set().filter(publish_at__lt=datetime.now()).filter(active=True)

class Poll(models.Model):
  created_at = models.DateTimeField(auto_now_add=True, default=datetime.now())
  updated_at = models.DateTimeField(auto_now=True)
  publish_at = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name='Publiceren op')
  active = models.BooleanField(default=False, verbose_name='Actief?')
  intro = models.TextField(null=True, blank=True)
  title = models.CharField(max_length=255)

  objects = models.Manager()
  publishable = ActivePollManager()

  class Meta:
    get_latest_by = 'publish_at'

  def can_vote(self,ip):
    try:
      from datetime import timedelta
      votes = Vote.objects.filter(poll=self).filter(ip=ip).filter(created_at__gte=datetime.now() - timedelta(minutes=5))
      print votes
      if len(votes) > 0:
        return False
      else:
        return True
    except:
      return True
  
  # vote the choice, let the backend figure out if a vote was possible
  def vote(self,ip, option):
    try:
      choice = Choice.objects.get(poll=self,pk=option)
      if choice:
        choice.count = choice.count + 1
        choice.save()

        vote = Vote()
        vote.ip = ip
        vote.choice_id = choice.id
        vote.poll = self
        vote.save()
        return True
      else:
        return False
    except:
      return False
  
  def votes(self):
    votes = Vote.objects.filter(poll=self).count()
    return votes
  
  @models.permalink
  def get_absolute_url(self):
    return ('PollResults', [self.id])

class Choice(models.Model):
  poll = models.ForeignKey('Poll')
  option = models.CharField(max_length=255, verbose_name='Optie')
  count =  models.PositiveIntegerField(max_length=255, default=0, verbose_name='Stemmen')
  
  def __unicode__(self):
    return self.option
    
  def percentage(self):
    if self.count == 0:
      return 0
    import math
    choices = Choice.objects.filter(poll=self.poll)
    total = 0
    for choice in choices:
      total = total + choice.count
    
    if total == 0:
      return 0
    percentage = (100 * self.count) / total
    return math.floor(percentage)
  
class Vote(models.Model):
  created_at = models.DateTimeField(auto_now_add=True, default=datetime.now())
  ip = models.IPAddressField()
  poll = models.ForeignKey('Poll')
  choice = models.ForeignKey('Choice')