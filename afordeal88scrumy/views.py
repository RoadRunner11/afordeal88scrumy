from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse 
from .models import User, ScrumyGoals, ScrumyHistory, GoalStatus
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignupForm, CreateGoalForm, MoveGoalForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import random
# Create your views here.
def index(request):
    goals = ScrumyGoals.objects.filter(goal_name='Learn Django')
    # for goal in goals:
    #     print(goal)
    #     return HttpResponse( goal )
    form = SignupForm()
    if request.method =="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            cd = form.cleaned_data
            userr = User.objects.create_user(username=cd['username'], password=form.cleaned_data['password'], email=cd['email'])
            userr.is_staff = True
            userr.is_superuser = True 
            my_group = Group.objects.get(name='Developer')
            my_group.user_set.add(userr)
            return redirect('success')
    else:
        form= SignupForm()
    return render(request, 'afordeal88scrumy/index.html', {'form':form})
def account_created(request):
    return render(request, 'afordeal88scrumy/success.html')

def move_goal(request, goal_id):
    error ='A record with that goal id does not exist'
    try:
        obj = ScrumyGoals.objects.get(goal_id=goal_id)
    except ScrumyGoals.DoesNotExist:
        return render(request, 'afordeal88scrumy/exception.html', {'error': error}) 
    else: 
        return HttpResponse(obj.goal_name)

def add_goal(request):
    if request.method == 'POST':
        goal_form = CreateGoalForm(request.POST)
        if goal_form.is_valid():
            cd = goal_form.cleaned_data
            add_gol = goal_form.save(commit=False)
            add_gol.goal_id = gen_id() #random.randint(1000, 9999)
            add_gol.created_by = cd['user']
            add_gol.moved_by = cd['user']
            add_gol.owner = cd['user']
            goal_status = cd['goal_status'].status_name
            add_gol.save()
            return redirect('home')
    else:
        goal_form = CreateGoalForm()
    return render(request,'afordeal88scrumy/add_goal.html', {'goal_form':goal_form} )

    # user = User.objects.get(username='louis')
    # goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
    # ScrumyGoals.objects.create(goal_name="Keep Learning Django", goal_id = gen_id(), created_by="Louis", 
    # moved_by = "Louis", owner="Louis", goal_status=goal_status, user=user )
    # return HttpResponse('Goal has been successgully added')
@login_required(login_url='accounts/login/')
def home(request):
    goals = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    users = User.objects.all()
    weekly = GoalStatus.objects.get(status_name="Weekly Goal")
    weekly = weekly.scrumygoals_set.all()
    daily = GoalStatus.objects.get(status_name="Daily Goal")
    daily = daily.scrumygoals_set.all()
    verify = GoalStatus.objects.get(status_name="Verify Goal")
    verify = verify.scrumygoals_set.all()
    done = GoalStatus.objects.get(status_name="Done Goal")
    done = done.scrumygoals_set.all()
    context = {
        'goals':goals,
        'users':users,
        'weekly':weekly,
        'daily':daily,
        'verify':verify,
        'done':done,
    }
    output = ', '.join([goal.goal_name for goal in goals])
    # print(request.user)
    return render(request, "afordeal88scrumy/home.html", context)

def gen_id():
        id_list = ScrumyGoals.objects.all()
        id_list = [idd.goal_id for idd in id_list]
        g_id = random.randint(1000, 9999)
        if g_id in id_list:
                g_id= random.randint(1000, 9999)
        return g_id