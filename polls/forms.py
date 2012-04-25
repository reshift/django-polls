from django.forms import ModelForm
from polls.models import *

class PollForm(ModelForm):
    class Meta:
        model=Poll