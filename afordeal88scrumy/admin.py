from django.contrib import admin
from .models import GoalStatus, ScrumyGoal, ScrumyHistory
# Register your models here.
admin.site.register (GoalStatus )
admin.site.register(ScrumyGoal)
admin.site.register(ScrumyHistory)