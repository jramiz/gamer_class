from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'class_app/index.html')

def register_user(request):
    error = User.objects.validate_registration(request.POST)
    if len(error):
        for key, value in error.items():
            messages.error(request, value)
        return redirect("/")
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    final_hashed_pw = hashed_pw.decode('utf-8')
    user = User.objects.create(user_name = request.POST['user_name'], email = request.POST['email'], password = final_hashed_pw)
    request.session['user_id'] = user.id
    return redirect('/dashboard')

def login_user(request):
    error = User.objects.validate_login(request.POST)
    if len(error):
        for key, value in error.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.get(email = request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/dashboard')

def dashboard(request):
    user = User.objects.get(id = request.session['user_id'])
    games = Game.objects.all()
    context = {
        "user" : user,
        "games" : games,
    }
    return render(request, 'class_app/dashboard.html', context)

def process_new_game(request):
    user = User.objects.get(id = request.session['user_id'])
    game = Game.objects.create(name=request.POST['name'], desc = request.POST['desc'], created_by = user)
    return redirect('/dashboard')

