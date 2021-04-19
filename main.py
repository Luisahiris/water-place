from flask import Flask, render_template, request, session, url_for, redirect, g
from src import api as apiResponses
from DB import database as db
from datetime import date
from src import helpers

app = Flask(__name__)

user = helpers.createUser(1, 'lu', 123456)

users = []
users.append(user)

app.secret_key = 'DAS211564a1sdjoNJU_djUYTF5245'

# @app.before_request
# def before_request():
#   if 'user_id' in session:
#     try:
#       user = [x for x in users if x.id == id][0]
#       g.user = user
#     except:
#       return

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    session.pop('user_id', None)

    username = request.form['username']
    password = request.form['password']

    user = [x for x in users if x.username == username][0]
    if user and user.password == password:
      session['user_id'] = user.id
      return redirect(url_for('/'))
    
    return redirect(url_for('login'))

  return render_template('logIn.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    session.pop('user_id', None)

    username = request.form['username']
    password = request.form['password']

    user = helpers.createUser(len(users), username, password)
    users.append(user)
    session['user_id'] = user.id
    return redirect(url_for('message'))
    
    # return redirect(url_for('signup'))

  return render_template('signUp.html')
 
@app.route('/')  
def message(): 
  apiProvincias = apiResponses.provincias()
  cul = db.crops.keys()
  return render_template('index.html', cultivos=cul, provincias=apiProvincias)

@app.route('/water-place', methods=['POST'])
def waterPlace():
  place = request.form['place']
  apiLatLong = apiResponses.latLong(place)
  lat, lon = apiLatLong["latitude"], apiLatLong["longitude"]
  apiEto = apiResponses.et_reference(lat, lon)
  et_reference = apiEto['evapotranspiration']

  cropping = request.form['cropping']

  dateForm = request.form['dateCroppin']
  year, month, day = dateForm.split('-')
  year, month, day = int(year), int(month), int(day)
  dateCrop = date(year, month, day)
  today = date.today()
  diffDays = 0
  if today != dateCrop:
    diffDays = today - dateCrop
    diffDays = str(diffDays).split(' ')[0]
    diffDays = int(diffDays)

  area = request.form['area']
  irrigationType = request.form['riego']

  user.setUp(dateForm, cropping, int(area), [lat, lon], diffDays, irrigationType)

  cropData = db.crops[cropping]
  rainResponse = apiResponses.weather(lat, lon)
  user.calculateNext7Days(cropData, et_reference, rainResponse)

  user.littersQuantity()

  time = helpers.convert(user.time * 3600)
  time = time.split(':')
  time = f'{time[0]} horas y {time[1]} minutos'
  
  helpers.saveUserData(user)

  return render_template('results.html', cultivo=cropping, time=time, period=user.period)

if __name__ == '__main__':
  app.run(debug = True) 