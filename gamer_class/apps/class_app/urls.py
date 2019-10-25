from django.conf.urls import url
from . import views

urlpatterns = [
    # External facing routes
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^hot$', views.hot),
    url(r'^class_list$', views.class_list),
    url(r'^schedule$', views.schedule),


    # Internal facing routes
    url(r'^register_user$', views.register_user),
    url(r'^login_user$', views.login_user),
    url(r'^add_game$', views.process_new_game),
    url(r'^process_new_game$', views.process_new_game),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment$', views.post_comment),
    url(r'^delete_message/(?P<id>\d+)$', views.delete_message),
    url(r'^delete_comment/(?P<id>\d+)$', views.delete_comment),
    url(r'^process_new_class$', views.process_new_class),
    url(r'^edit_class$', views.edit_class),
    url(r'^logout$', views.logout),
    url(r'^class/delete/(?P<gamer_id>\d+)$', views.delete),

]