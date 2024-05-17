from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', home, name = 'home'),
    path('contacts/', contacts, name = 'contacts'),
    path('standings/', standings, name = 'standings'),
    path('teams/', teams, name = 'teams'),
    path('news/', news, name = 'news'),
    path('schedule/', schedule, name = 'schedule'),
    path('sign_in/', sign_in, name = 'sign_in'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_out/', sign_out, name='sign_out'),
    path('team/<int:pk>', team, name='team'),
    path('article/<int:news_id>', article, name='article')
]