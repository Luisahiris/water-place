import requests
from flask import redirect

def api(url):
    try:
        response = requests.get(url)
    except:
        return redirect('/')

    return response.json()

def weather(lat, lon):
    lat, lon = lat, lon
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely&lang=es&appid=22c3c6556377ef7aa668297808e841ae".format(lat, lon)

    weather = api(url)
    rains = []
    waterRain = 0
    try:
        for day in weather['daily']:
            if 'rain' in day:
                waterRain += int(day['rain'])
                rains.append(day['rain'])
    except:
        return redirect('/')

    return waterRain

def provincias():
    urlProvincias = "http://provinciasrd.raydelto.org/provincias"
    response = api(urlProvincias)

    return response["data"]

def latLong(place):
    query = place.replace(" ", "%20")
    url = "http://api.positionstack.com/v1/forward?access_key=cdae9836cb283b23d1416bb0af7fb7db&query={}".format(query)

    response = api(url)

    return response["data"][0]

def et_reference(lat, long):
    key = "47744cc6c9cf403183849279546fc1b2"
    url = "https://api.weatherbit.io/v2.0/forecast/agweather?lat={}&lon={}&key={}".format(lat, long, key)

    response = api(url)

    return response["data"][0]
