from django.shortcuts import render
from django.http import HttpResponse 
from .models import User, ScrumyGoals, ScrumyHistory, GoalStatus
from django.core.exceptions import ObjectDoesNotExist
import random
# Create your views here.
def index(request):
    goals = ScrumyGoals.objects.filter(goal_name='Learn Django')
    for goal in goals:
        print(goal)
        return HttpResponse( goal )

def move_goal(request, goal_id):
    error ='A record with that goal id does not exist'
    try:
        obj = ScrumyGoals.objects.get(goal_id=goal_id)
    except ScrumyGoals.DoesNotExist:
        return render(request, 'afordeal88scrumy/exception.html', {'error': error}) 
    else: 
        return HttpResponse(obj.goal_name)

def add_goal(request):
    user = User.objects.get(username='louis')
    goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
    ScrumyGoals.objects.create(goal_name="Keep Learning Django", goal_id = gen_id(), created_by="Louis", 
    moved_by = "Louis", owner="Louis", goal_status=goal_status, user=user )
    return HttpResponse('Goal has been successgully added')

def home(request):
    goals = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    scrumg = ScrumyGoals.objects.get(goal_name="Learn Django")
    user = scrumg.user
    goal_id = scrumg.goal_id
    goal_name = scrumg.goal_name
    context = {
        'user':user,
        'goal_id':goal_id,
        'goal_name':goal_name,       
    }
    output = ', '.join([goal.goal_name for goal in goals])
    return render(request, "afordeal88scrumy/home.html", context)

def gen_id():
        id_list = ScrumyGoals.objects.all()
        id_list = [idd.goal_id for idd in id_list]
        g_id = random.randint(1000, 9999)
        if g_id in id_list:
                g_id= random.randint(1000, 9999)
        return g_id