from flask import Flask, render_template, request
from src import api as apiResponses
from DB import database as db
from datetime import date
from src import helpers

app = Flask(__name__)

user = helpers.createUser(1, 'lu', 123456)
 
@app.route('/')  
def message(): 
  apiProvincias = apiResponses.provincias()
  cul = db.cultivos
  return render_template('index.html', cultivos=cul, provincias=apiProvincias)

@app.route('/water-place', methods=['POST'])
def waterPlace():
  place = request.form['place']
  apiLatLong = apiResponses.latLong(place)
  lat, lon = apiLatLong["latitude"], apiLatLong["longitude"]
  apiEto = apiResponses.et_reference(lat, lon)
  et_reference = apiEto['evapotranspiration']

  cropping = request.form['cropping'].lower()
  # cropKCs = db.crops[cropping]['kc']

  dateForm = request.form['dateCroppin']
  year, month, day = dateForm.split('-')
  year, month, day = int(year), int(month), int(day)
  dateCrop = date(year, month, day)
  today = date.today()
  diffDays = today - dateCrop
  diffDays = str(diffDays).split(' ')[0]

  area = request.form['area']
  irrigationType = request.form['riego']

  periods = {
    'init': { 'etc': 0, 'rain': 0, 'missing': 0, 'litters': 0, 'completed': False },
    'dev': { 'etc': 0, 'rain': 0, 'missing': 0, 'litters': 0, 'completed': False },
    'mid': { 'etc': 0, 'rain': 0, 'missing': 0, 'litters': 0, 'completed': False },
    'end': { 'etc': 0, 'rain': 0, 'missing': 0, 'litters': 0, 'completed': False },
  }

  user.setUp(dateForm, cropping, area, [lat, lon], periods)

  for key in periods.keys():
    periodKc = db.crops[cropping]['kc'][key]
    periodDays = db.crops[cropping]['days'][key]

    periodEtc = periodKc * et_reference * periodDays
    

    periods[key]['etc'] = periodEtc

    rainResponse = apiResponses.weather(lat, lon, periodDays)

    periods[key]['rain'] += rainResponse

    periods[key]['missing'] = periodEtc - rainResponse

    if periods[key]['missing'] >= 0:
       periods[key]['litters'] = helpers.littersQuantity(periods[key]['missing'], int(area), irrigationType)
    else:
      periods = helpers.leftOverRain(key, periods)


  return render_template('results.html', lugar=place, cultivo=cropping, lat=lat, lon=lon, date=diffDays, periods=str(periods), area=area)

if __name__ == '__main__':
  app.run(debug = True) 