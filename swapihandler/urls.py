from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'swapihandler'
urlpatterns = [
    path('', views.index, name='index'),
    path('moviedetail/<int:number>', views.movie_detail, name='moviedetail'),
    path('characterdetail/<int:number>', views.character_detail, name='charaterdetail'),
    path('planetdetail/<int:number>', views.planet_detail, name='planetdetail'),
    path('starshipdetail/<int:number>', views.starship_detail, name='starshipdetail'),
    url(r'^search-form/$', views.search_form),
    url(r'^searchview/$', views.search),
    ]
