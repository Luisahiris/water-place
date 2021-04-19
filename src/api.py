import requests

def api(url):
    response = requests.get(url)

    return response.json()

def weather(lat, lon, days):
    lat, lon = lat, lon
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely&lang=es&appid=81a2eda3859b3d2d3993e10076a2f55b".format(lat, lon)

    weather = api(url)
    rains = []
    waterRain = 0

    for day in weather['daily']:
        if 'rain' in day:
            waterRain += int(day['rain'])
            rains.append(day['rain'])

    # i = 0
    # while i < days:
    #     response = api(url)

    #     for daily in response['daily']:
    #         if 'rain' in daily:
    #             waterRain += int(daily['rain'])
    #             rains.append(daily['rain'])
        
    #     i += 1

    return waterRain

def provincias():
    urlProvincias = "http://provinciasrd.raydelto.org/provincias"
    response = api(urlProvincias)

    return response["data"]

def latLong(place):
    query = place.replace(" ", "%20")
    url = "http://api.positionstack.com/v1/forward?access_key=903afabb8803c4faf82c58296f2ba4f3&query={}".format(query)

    response = api(url)

    return response["data"][0]

def et_reference(lat, long):
    key = "47744cc6c9cf403183849279546fc1b2"
    url = "https://api.weatherbit.io/v2.0/forecast/agweather?lat={}&lon={}&key={}".format(lat, long, key)

    response = api(url)

    return response["data"][0]
