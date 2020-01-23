from django.shortcuts import render
from django.http import HttpResponse 
from .models import User, ScrumyGoals, ScrumyHistory, GoalStatus
import random
# Create your views here.
def index(request):
    goals = ScrumyGoals.objects.filter(goal_name='Learn Django')
    for goal in goals:
        print(goal)
        return HttpResponse( goal )

def move_goal(request, goal_id):
    goal_name = ScrumyGoals.objects.get(goal_id = goal_id)
    return HttpResponse(goal_name)

def add_goal(request):
    user = User.objects.get(username='louis')
    goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
    ScrumyGoals.objects.create(goal_name="Keep Learning Django", goal_id = gen_id(), created_by="Louis", 
    moved_by = "Louis", owner="Louis", goal_status=goal_status, user=user )
    return HttpResponse('Goal has been successgully added')

def home(request):
    goals = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    output = ', '.join([goal.goal_name for goal in goals])
    return HttpResponse(output)

def gen_id():
        id_list = ScrumyGoals.objects.all()
        id_list = [idd.goal_id for idd in id_list]
        g_id = random.randint(1000, 9999)
        if g_id in id_list:
                g_id= random.randint(1000, 9999)
        return g_id