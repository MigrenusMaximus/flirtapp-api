from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^authenticate/$', views.authenticate, name='authenticate'),
    url(r'^update_fcm_id/$', views.update_fcm_id, name='update_fcm_id'),
    url(r'^upload_photo/$', views.upload_photo, name='upload_photo'),
    url(r'^login/$', views.login, name='login'),
    url(r'^select_likes/$', views.select_likes, name='select_likes'),
    url(r'^update_users/$', views.update_users, name='update_users'),
    url(r'^get_matches/$', views.get_matches, name='get_matches'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^get_messages/$', views.get_messages, name='get_messages'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^get_location_info/$', views.get_location_info, name='get_location_info'),
    url(r'^get_user_counts/$', views.get_user_counts, name='get_user_counts'),
]
