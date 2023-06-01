from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('play/<int:row>/<int:col>/', views.play, name='play'),
    path('reset/', views.reset, name='reset'),
    path('undo/', views.undo, name='undo')
]