import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

API_KEY = 'OPEN_WEATHER_API_KEY'
API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'


def index(request):

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    
       
    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:

        response = requests.get(API_URL.format(city, API_KEY)).json()

        try:

            city_weather = {
                'city': city.name,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }

            weather_data.append(city_weather)
        
        except:
            pass
        

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/weather.html', context)