from django.shortcuts import render
from django.http import HttpResponse 
from .models import User, ScrumyGoals, ScrumyHistory, GoalStatus
# Create your views here.
def index(request):
    goals = ScrumyGoals.objects.filter(goal_name='Learn Django')
    for goal in goals:
        print(goal)
        return HttpResponse( goal )
def move_goal(request, goal_id):
    goal_name = ScrumyGoals.objects.get(goal_id = goal_id)
    return HttpResponse(goal_name)