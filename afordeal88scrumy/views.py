from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse 
from django.contrib import messages
from .models import User, ScrumyGoals, ScrumyHistory, GoalStatus
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignupForm, CreateGoalForm, MoveGoalForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout
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
def logout_view(request):
    logout(request)
    redirect('login')
# @login_required(login_url='accounts/login/')
def move_goal(request, goal_id):
    context = {'goal_id':goal_id}
    move_form = MoveGoalForm()
    current_user = request.user
    group= None
    if current_user.username == 'louis':
        group
    else:
        group = current_user.groups.all()[0]
    try:
        
        current_user = request.user

        users_in_dev = Group.objects.get(name="Developer").user_set.all()
        users_in_QA = Group.objects.get(name="Quality Assurance").user_set.all()
        users_in_adm = Group.objects.get(name="Admin").user_set.all()
        users_in_own = Group.objects.get(name="Owner").user_set.all()
        instance = ScrumyGoals.objects.get(goal_id=goal_id)
        
        if request.method == 'POST':
            move_form = MoveGoalForm(request.POST, instance=instance)
            if move_form.is_valid():
                mover = move_form.save(commit=False)
                cd = move_form.cleaned_data
                goal_status = cd['goal_status'].status_name
                # print(current_user)
                user = mover.user
                # return render(request, 'afordeal88scrumy/error_move.html', 
                #     {   'current_user':current_user,
                #         'users_in_dev':users_in_dev,
                #         'users_in_QA':users_in_QA,
                #         'users_in_adm':users_in_adm,
                #         'users_in_own':users_in_own,
                #         'move_form':move_form,
                #         'goal_status':goal_status,
                #         'mover':mover,

                        # })
                if current_user in users_in_dev and goal_status == 'Done Goal':
                    messages.error(request, ' Access restricted, as a DEv, You cannot move to Done goals')
                    return HttpResponseRedirect(request.path)
                    # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">\
                    # Access restricted, as a DEv, You cannot move to Done goals</span>') 
                          
                elif current_user in users_in_dev and current_user!= user:
                    messages.error(request, " Access restricted, as a DEv, You cannot move other users' goal")
                    # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">\
                    # Access restricted, as a Dev, You cannot move other users goals</span>')        
                    return HttpResponseRedirect(request.path)    
                elif current_user in users_in_QA and goal_status=='Weekly Goal':
                    messages.error(request, " Access restricted,as a QA, You cannot move back to Weekly goals")
                    return HttpResponseRedirect(request.path)
                    # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">\
                    # Access restricted,as a QA, You cannot move back to Weekly goals</span>')

                elif current_user in users_in_QA and current_user != user and mover.goal_status.status_name!='Verify Goal' and goal_status!= 'Done Goal':
                    messages.error(request, " Access restricted,as a QA, You cannot move back to Weekly goals")
                    return HttpResponseRedirect(request.path)
                    # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">\
                    #     Access restricted,as a QA, You can only move other people goal from \
                    # verify goal to done goal </span>')

                elif current_user in users_in_own and current_user != user:
                    messages.error(request, " Access restricted,as a QA, You cannot move back to Weekly goals")
                    return HttpResponseRedirect(request.path)
                    # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">\
                    #     Access restricted,as an owner, You can only move your goals</span>')
                else:
                    post = mover.save()
                    return redirect('home')

            else:
                move_form = MoveGoalForm(instance=instance)                        


    except ObjectDoesNotExist:
        return render(request, 'afordeal88scrumy/exception.html', context)
        
    return render(request, 'afordeal88scrumy/move_goal.html', {
        'current_user':current_user,
        'users_in_dev':users_in_dev,
        'users_in_QA':users_in_QA,
        'users_in_adm':users_in_adm,
        'users_in_own':users_in_own,
        'move_form':move_form,

    }) 
@login_required(login_url='accounts/login/')
def add_goal(request):
    current_user = request.user
    group=None
    if current_user.username == 'louis':
        group
    else:
        group = current_user.groups.all()[0]
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
            users_in_dev = Group.objects.get(name="Developer").user_set.all()
            users_in_QA = Group.objects.get(name="Quality Assurance").user_set.all()
            users_in_adm = Group.objects.get(name="Admin").user_set.all()
            users_in_own = Group.objects.get(name="Owner").user_set.all()
            # print(current_user)
            # print(cd['user'])
            if current_user in users_in_dev and current_user != cd['user']:
                # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">Access restricted, as a Dev,\
                #         You can only create weekly goal for yourself</span>')
                messages.error(request, "Access restricted, as a Dev, You can only create weekly goal for yourself ")
                return HttpResponseRedirect(request.path)
            if current_user in users_in_dev and goal_status != 'Weekly Goal' :
                # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">Access restricted, as a Dev,\
                #         You can only create tasks under Weekly goals</span>')
                messages.error(request, "Access restricted, as a Dev, You can only create weekly goal for yourself ")
                return HttpResponseRedirect(request.path)
            if current_user in users_in_QA and current_user != cd['user']:
                # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">Access restricted, as a QA,\
                #         You can only create weekly goal for yourself</span>') 
                messages.error(request, "Access restricted, as a QA, You can only create weekly goal for yourself ")
                return HttpResponseRedirect(request.path)
            if current_user in users_in_adm and current_user != cd['user']:
                    #  return HttpResponse('<span style="background-color:red;color:white;padding:10px;">Access restricted,
                    #  You can only create weekly goal for yourself</span>')  
                messages.error(request, "Access restricted, as a Admin, You can only create weekly goal for yourself ")
                return HttpResponseRedirect(request.path)          
            if current_user in users_in_own and current_user != cd['user']:
                # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">Access restricted, as an owner
                #         You can only create weekly goal for yourself</span>') 
                messages.error(request, "Access restricted, as an Owner, You can only create weekly goal for yourself ") 
                return HttpResponseRedirect(request.path)           
            else:
                    # ScrumyGoal.objects.create(
                    # goal_name=cd['goal_name'], goal_id=gen_id(), created_by=cd['user'], 
                    # moved_by= cd['user'], owner=cd['user'], goal_status=GoalStatus(1), user=User.objects.get(username=cd['user']) )
                add_gol.save()
                return redirect('home')
                # return HttpResponse('<span style="background-color:red;color:white;padding:10px;">Added successfully</span>')   
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
    current_user = request.user
    group = None
    # print(current_user=='louis')
    # print(current_user.username)
    if current_user.username == 'louis':
        group = group
    else:
        group = current_user.groups.all()[0]
    context = {
        'goals':goals,
        'users':users,
        'weekly':weekly,
        'daily':daily,
        'verify':verify,
        'done':done,
        'current_user':current_user,
        'group':group,
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