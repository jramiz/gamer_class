from django.conf.urls import url
from . import views

urlpatterns = [
    # External facing routes
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),


    # Internal facing routes
    url(r'^register_user$', views.register_user),
    url(r'^login_user$', views.login_user),
    url(r'^process_new_game$', views.process_new_game),
]