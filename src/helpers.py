import datetime

class User():
  def __init__(self, id, username, password):
    self.id = id
    self.username = username
    self.password = password

  def setUp(self, dateStarted, cropping, area, location, days, irrigationType):
    self.dateStarted = dateStarted
    self.cropping = cropping
    self.irrigationType = irrigationType
    self.area = area
    self.location = location
    self.period = 'Inicial'
    self.daysCount = 0
    self.littersApplied = 0
    self.currentEtc = 0
    self.currentRain = 0
    self.missing = 0
    self.status = 'inProgress'
    self.litters = 0
    self.time = 0

  def update(self, etc, rain):
    self.currentEtc = etc
    self.currentRain = rain
    self.missing += etc - rain

  def calculateNext7Days(self, cropData, et0, rainResponse):
    daysCount = self.daysCount + 7
    if daysCount > cropData['days']['total']:
      currentEtc = cropData['kc']['end'] * et0 * (cropData['days']['total'] - self.daysCount)

      self.update(currentEtc, rainResponse)
      self.status = 'Completed'
      return

    for key in cropData['days']:
      if key != 'total' and cropData['days'][key] > self.daysCount:
        self.daysCount += 7
        subs = cropData['days'][key] - self.daysCount

        if subs < 0:
          currentEtc = cropData['kc'][key] * et0 * (subs + 7)
          nextEtc = cropData['kc'][key] * et0 * (subs * -1)

          self.update(currentEtc + nextEtc, rainResponse)
          self.period = nextPeriod(key)

        else:
          currentEtc = cropData['kc'][key] * et0 * 7
          self.update(currentEtc, rainResponse)

        return
  
  def littersQuantity(self):
    litters = self.missing * self.area
    addition = 0
    
    if self.irrigationType == 'Aspersión':
      addition = 0.30
    elif self.irrigationType == 'Microaspersión':
      addition = 0.15
    
    litters = litters + (litters * addition)

    self.litters = litters
    self.littersApplied += litters
    self.missing = 0

    self.littersPerMinute()

  def littersPerMinute(self):
    irrigation = self.area / 36
    littersCapacity = irrigation * 1000

    results = self.litters / littersCapacity
    
    self.time = results

def createUser(id, username, password):
  newUser = User(id, username, password)

  return newUser

def nextPeriod(key):
  periods = [
    'Inicial',
    'Desarrollo',
    'Medio',
    'Final'
  ]

  index = periods.index(key)

  return periods[index + 1]

def convert(n):
    return str(datetime.timedelta(seconds = n))

def saveUserData(user):
  data = ['\n'+str(user.username)+'-', str(user.password)+'-', str(user.period)+'-', str(user.littersApplied)+'-', str(user.daysCount)]
  file = open('users.txt', 'a')

  file.writelines(data)

  file.close()
