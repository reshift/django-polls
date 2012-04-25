from django.contrib import admin
from polls.models import *

class ChoiceInline(admin.StackedInline):
  model = Choice
  verbose_name = "Optie"
  extra = 5
  classes = ('collapse-open','open')
  fieldsets = (
      ('', {
        'classes': ('collapse-open',),
        'fields': ('option','count',),
      }),
    )
  readonly_fields = ('count',)

class PollAdmin(admin.ModelAdmin):
  inlines = [ChoiceInline,]
  search_fields = ['title','intro']
  date_hierarchy = 'publish_at'
  list_display_links = ('title',)
  list_display = ('publish_at', 'title', 'active')
  
  fieldsets = (
      ('', {
        'fields': ('publish_at','active','title','intro',),
      }),
    )
  

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)

