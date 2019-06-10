from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import json


def index(request):
    r = requests.get('https://swapi.co/api/films')
    datos = r.json()
    template = loader.get_template('swapihandler/index.html')
    id = 0
    for i in datos['results']:
        id += 1
        req = requests.get('https://swapi.co/api/films/{}'.format(id))
        req = req.json()
        for j in datos['results']:
            if j["episode_id"] == req["episode_id"]:
                j.update({'id':id})

    context = {
        'datos': datos,
    }
    return HttpResponse(template.render(context, request))

def movie_detail(request, number):
    r = requests.get('https://swapi.co/api/films/{}'.format(number))
    datos = r.json()
    template = loader.get_template('swapihandler/moviedetail.html')
    characters = {}
    planets = {}
    starships = {}
    for url in datos['characters']:
        reqchar = requests.get('{}'.format(url)).json()
        nombre = reqchar['name']
        url = url.split('/')
        id = url[-2]
        characters.update({nombre:id})
    for url in datos['planets']:
        reqplan = requests.get('{}'.format(url)).json()
        nombre = reqplan['name']
        url = url.split('/')
        id = url[-2]
        planets.update({nombre:id})
    for url in datos['starships']:
        reqships = requests.get('{}'.format(url)).json()
        nombre = reqships['name']
        url = url.split('/')
        id = url[-2]
        starships.update({nombre:id})
    context = {
        'movie': datos,
        'characters': characters,
        'planets': planets,
        'starships': starships,

    }
    return HttpResponse(template.render(context, request))


def character_detail(request, number):
    r = requests.get('https://swapi.co/api/people/{}'.format(number))
    datos = r.json()
    template = loader.get_template('swapihandler/characterdetail.html')
    planets = {}
    movies = {}
    starships = {}
    reqplan = requests.get('{}'.format(datos['homeworld'])).json()
    nombre = reqplan['name']
    url = datos['homeworld'].split('/')
    id = url[-2]
    planets.update({nombre:id})

    for link in datos['films']:
        reqmov = requests.get('{}'.format(link)).json()
        nombre = reqmov['title']
        url = link.split('/')
        id = url[-2]
        movies.update({nombre:id})

    for link in datos['starships']:
        reqstar = requests.get('{}'.format(link)).json()
        nombre = reqstar['name']
        url = link.split('/')
        id = url[-2]
        starships.update({nombre:id})

    context = {
        'datos': datos,
        'planets': planets,
        'movies': movies,
        'starships': starships,
        }
    return HttpResponse(template.render(context, request))



def planet_detail(request, number):
    r = requests.get('https://swapi.co/api/planets/{}'.format(number))
    datos = r.json()
    template = loader.get_template('swapihandler/planetdetail.html')
    residents = {}
    films = {}
    for link in datos['residents']:
        reqres = requests.get('{}'.format(link)).json()
        nombre = reqres['name']
        url = link.split('/')
        id = url[-2]
        residents.update({nombre:id})

    for link in datos['films']:
        reqfilms = requests.get('{}'.format(link)).json()
        nombre = reqfilms['title']
        url = link.split('/')
        id = url[-2]
        films.update({nombre:id})


    context = {
        'datos': datos,
        'residents': residents,
        'films': films,
        }
    return HttpResponse(template.render(context, request))




def starship_detail(request, number):
    r = requests.get('https://swapi.co/api/starships/{}'.format(number))
    datos = r.json()
    pilots = {}
    template = loader.get_template('swapihandler/starshipdetail.html')
    films = {}
    for link in datos['pilots']:
        reqpilots = requests.get('{}'.format(link)).json()
        nombre = reqpilots['name']
        url = link.split('/')
        id = url[-2]
        pilots.update({nombre:id})
    for link in datos['films']:
        reqfilms = requests.get('{}'.format(link)).json()
        nombre = reqfilms['title']
        url = link.split('/')
        id = url[-2]
        films.update({nombre:id})
    context = {
        'datos': datos,
        'pilots': pilots,
        'films': films,
        }
    return HttpResponse(template.render(context, request))


def search_form(request):
    return render(request, 'swapihandler/searchview.html')

def search(request):
    if 'q' in request.GET:
        message = '%r' % request.GET['q']
        template = loader.get_template('swapihandler/searchview.html')
        characters = []
        films = []
        starships = []
        planets = []
        reqpeople = requests.get('https://swapi.co/api/people/?search={}'.format(request.GET['q'])).json()
        while True:
            for personaje in reqpeople['results']:
                id = personaje['url'].split('/')[-2]
                personaje.update({"id":id})
                characters.append(personaje)
            if (reqpeople['next']):
                reqpeople = requests.get('{}'.format(reqpeople['next'])).json()
            else:
                break

        reqfilms = requests.get('https://swapi.co/api/films/?search={}'.format(request.GET['q'])).json()
        while True:
            for film in reqfilms['results']:
                id = film['url'].split('/')[-2]
                film.update({"id":id})
                films.append(film)
            if (reqfilms['next']):
                reqfilms = requests.get('{}'.format(reqfilms['next'])).json()
            else:
                break

        reqstarships = requests.get('https://swapi.co/api/starships/?search={}'.format(request.GET['q'])).json()
        while True:
            for starship in reqstarships['results']:
                id = starship['url'].split('/')[-2]
                starship.update({"id":id})
                starships.append(starship)
            if (reqstarships['next']):
                reqstarships = requests.get('{}'.format(reqstarships['next'])).json()
            else:
                break

        reqplanets = requests.get('https://swapi.co/api/planets/?search={}'.format(request.GET['q'])).json()
        while True:
            for planet in reqplanets['results']:
                id = planet['url'].split('/')[-2]
                planet.update({"id":id})
                planets.append(planet)
            if (reqplanets['next']):
                reqplanets = requests.get('{}'.format(reqplanets['next'])).json()
            else:
                break


        context = {
            'message': message,
            'characters': characters,
            'films': films,
            'starships': starships,
            'planets': planets,
            }
    return HttpResponse(template.render(context, request))
