from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Veg, Input, Profile, STAGES, User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#turning serialize querysets with django objects to dictionary
from django.forms.models import model_to_dict

#login and signup
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

#User Signup function
def signup(request):
    error_message = ""

    #if signup is post, do this
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            #create a profile and add user
            profile = Profile.objects.create(
                name = user.username,
                user = user,
                expenses = 0.0,
            )

            login(request, user)
            return redirect('about')
        
        else:
            error_message= form.errors

    #if GET request or something else, 
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def veggies_index(request):

    #show only vegetables that has this user
    veggies = Veg.objects.all().filter(user_id=request.user.id)
    
    #grab the cost with this user profile
    profile = Profile.objects.get(user_id = request.user.id)
    expenses = profile.expenses
    #print(f'total expenses on this profile is {expenses}')

    return render(request, 'veggies/index.html', { 'veggies': veggies, "expenses": expenses })

#makes form for adding veggie
def veggies_create(request):
    #update later to to be just seeds in basket.
    seeds = Input.objects.all().filter(category='Seeds')
    print (seeds)

    seedslist = []

    for seed in seeds:

        seedobj = {}
        seedobj['name'] = seed.name
        seedobj['category'] = seed.category
        seedobj['description'] = seed.description
        seedobj['cost'] = seed.cost
        seedslist.append(seedobj)

    return render(request, 'veggies/veg_form.html', { 'seeds': seeds, 'stages': STAGES, "seedslist": seedslist})



def veggies_add(request):

    if request.method == 'POST':
        
      print(f'new vegetable planted is {request.POST["planted"]}')
      

      profile = Profile.objects.get(user_id=request.user.id)
      
      veg = Veg.objects.create(
          name = request.POST["name"],
          description= request.POST["description"],
          cost = request.POST["cost"],
          date = request.POST["date"],
          planted = request.POST["planted"],
          user = profile,
          stage = request.POST["stage"],
      )

      #updating the cost
      totalexpenses = profile.expenses
      cost = float(request.POST["cost"])
      planted = int(request.POST["planted"])
      print(f'TOTAL EXPENSES SO FAR: {totalexpenses}, cost is {cost} and planted number is {planted}')

      expenses = cost*planted
      # print(f'profile expense is {totalexpenses} and additional cost is {expenses}')
      #update cost and round to 2 decimal places
      totalexpenses = round(totalexpenses+expenses, 2)
      print(f'Total expenses is now {totalexpenses}')

      profile.expenses = totalexpenses
      profile.save()


    
    #return redirect('veg_create')
    return redirect('index')


#this adds a new kind of vegetable to the store, does not include date, planted or stage
class VegCreate(CreateView):
    
    model = Veg    

    fields = [ 'name', 'description', 'cost' ]
    success_url= '/veggies/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#there will be a seperate create to add instances of a vegetable to a garden

class InputList(ListView):
  model = Input

class InputDetail(DetailView):
  model = Input

class InputCreate(CreateView):
  model = Input
  fields = '__all__'
  success_url = '/inputs/'

class InputUpdate(UpdateView):
  model = Input
  fields = ['name', 'category', 'description', 'cost']
  success_url = '/inputs/'

class InputDelete(DeleteView):
  model = Input
  success_url = '/inputs/'

def inputs_index(request):
  inputs = Input.objects.all()
  return render(request, 'main_app/input_list.html', { 'inputs': inputs })


def veg_detail(request, veg_id):
    veg = Veg.objects.get(id=veg_id)
    p = Profile.objects.get(user_id=request.user.id)
    inputs_user = p.inputs.all()


    #update stages to display properly

    tempstage = veg.stage
    for idx in STAGES:
      if tempstage == idx[0]:
        veg.stage = idx[1]

    expenses = p.expenses

    return render(request, 'veggies/detail.html', { 'veg': veg, 'inputs_user': inputs_user, 'expenses': expenses })

def garden_store(request):
  p = Profile.objects.get(user_id=request.user.id)
  inputs_user = p.inputs.all()
  inputs = Input.objects.all()
  veggies = Veg.objects.all()
  return render(request, 'main_app/garden_store.html', { 'veggies': veggies, 'inputs': inputs, 'inputs_user': inputs_user })


def assoc_input(request, input_id):
  userid = request.user.id
  Profile.objects.get(user_id=userid).inputs.add(input_id)
  return redirect('garden_store')


def unassoc_input(request, input_id):
  userid = request.user.id
  Profile.objects.get(user_id=userid).inputs.remove(input_id)
  return redirect('garden_store')