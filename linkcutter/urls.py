from django.urls import path

from .views import *


app_name = 'linkcutter'
urlpatterns = [
    path('', index, name="index"),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('cut/', cutter, name='cutter'),
    path('link_list/', LinksListView.as_view(), name='link_list'),
    path('<str:short_link>', jump_to_target, name="jump_to_target"),
]