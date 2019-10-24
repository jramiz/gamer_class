from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import re

IMAGE_REGEX = re.compile(r'^([/|.|\w|\s|-])*.(?:jpg|jpeg|gif|png)')

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

def post_message(request):
    if request.method == "POST":
        errors = {}
        image = request.FILES.get('image', 'default_image.png')
        if not IMAGE_REGEX.match(str(image)):
            errors['image'] = "Please enter a .jpg, .jpeg, .png file for your image"
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/hot')
        if len(errors) > 0:
            return redirect('/hot')
        else:
            new_message= Message.objects.create(
                message = request.POST['message'],
                user = User.objects.get(id=request.session["user_id"]),
                image = image
            )
        return redirect("/hot")

def post_comment(request):
    user = User.objects.get(id=request.session["user_id"])
    message = Message.objects.get(id=request.POST['message_id'])
    new_comment = Comment.objects.create(comment=request.POST['comment'], user = user, message = message)
    return redirect("/hot")

def hot(request):
    context = {
        "user" : User.objects.get(id = request.session['user_id']),
        "messages" : Message.objects.all(),
        # "comments" : Comment.objects.all(),
    }
    return render(request, 'class_app/hot.html', context)

def delete_message(request, id):
    deleted_message=Message.objects.get(id=id)
    deleted_message.delete()
    return redirect('/hot')

def delete_comment(request, id):
    deleted_comment=Comment.objects.get(id=id)
    deleted_comment.delete()
    return redirect('/hot')

def class_list(request):
    user = Gamer.user.get(id = request.session['user_id']),
    context = {
        "gamer" : Gamer.objects.get(user = user)
    }
    return render(request, 'class_app/class.html', context)

def schedule(request):
    user = User.objects.get(id = request.session['user_id'])
    other_users = User.objects.exclude(id = request.session['user_id'])
    context = {
        "user" : user,
        "other_users" : other_users
    }
    return render(request, "class_app/schedule.html", context)
