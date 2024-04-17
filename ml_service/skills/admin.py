from django.contrib import admin

from .models import Category, Skill, Job, JobGuide

admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(JobGuide)
