from __future__ import unicode_literals
from django.db import models
import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_registration(self, post):
        error = {}
        if len(post['user_name']) < 8:
            error['first_name'] = "Your username must be at least 8 characters"
        if not EMAIL_REGEX.match(post['email']):
            error['email'] = "Enter a valid email format"
        if User.objects.filter(email=post['email']):
            error['emailDupe'] = "Your email and account already exist"
        if len(post['password']) < 8:
            error['password'] = "Your password must be at least 8 characters"
        if post['password'] != post['c_password']:
            error['pw_match'] = "Your passwords do not match"
        return error
    def validate_login(self, post):
        error = {}
        if not EMAIL_REGEX.match(post['email']):
            error['email'] = "Enter a valid email format"
        user = User.objects.filter(email = post['email'])
        if not user:
            error['loginemail'] = 'Email does not exist'
            return error
        if bcrypt.checkpw(post['password'].encode(), user[0].password.encode()):
            pass
        else:
            error['password'] = "Your password is incorrect"
        return error

class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 
    # games_added - related to Game
    # gamer_classes - related to Gamer

class Game(models.Model):
    name = models.TextField()
    desc = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name = "games_added")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # gamers - related to Gamer

class Gamer(models.Model):
    user = models.ForeignKey(User, related_name = "gamer_classes")
    game = models.ForeignKey(Game, related_name = "gamers")
    level = models.TextField()
    income = models.IntegerField()
    style = models.TextField()
    gamer_class = models.TextField()



