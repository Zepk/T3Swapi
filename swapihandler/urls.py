from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'swapihandler'
urlpatterns = [
    path('', views.index, name='index'),
    path('moviedetail/<str:number>', views.movie_detail, name='moviedetail'),
    path('characterdetail/<str:number>', views.character_detail, name='charaterdetail'),
    path('planetdetail/<str:number>', views.planet_detail, name='planetdetail'),
    path('starshipdetail/<str:number>', views.starship_detail, name='starshipdetail'),
    url(r'^search-form/$', views.search_form),
    url(r'^searchview/$', views.search),
    ]
