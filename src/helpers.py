class User():
  def __init__(self, id, username, password):
    self.id = id
    self.username = username
    self.password = password

  def setUp(self, dateStarted, cropping, area, location, periods, days):
    self.dateStarted = dateStarted
    self.cropping = cropping
    self.area = area
    self.location = location
    self.periods = periods
    self.daysCount = days
    self.littersApplied = 0

  def history(self, daysCount, littersApplied):
    self.daysCount = daysCount
    self.littersApplied = littersApplied

  def update(self, key, nextKey, etc, rain):
    self.periods[key]['etc'] = etc
    self.periods[key]['rain'] += rain
    self.periods[key]['missing'] = etc - rain

    if etc - rain < 0:
      self.periods[nextKey]['rain'] -= etc - rain

  def calculateNext7Days(self, cropData, et0, rainResponse):
    periodsIncompleted = self.incompletedPeriods()
    self.daysCount += 7

    if (cropData['days'][periodsIncompleted[0]] - self.daysCount) >= 7:

      periodEtc = cropData['kc'][periodsIncompleted[0]] * et0 * 7

      self.update(periodsIncompleted[0], periodsIncompleted[1], periodEtc, rainResponse)

      if (cropData['days'][periodsIncompleted[0]] - self.daysCount) == 7:
        self.periods[periodsIncompleted[0]]['completed'] = True
    else:
      current = cropData['days'][periodsIncompleted[0]] - self.daysCount
      nextDays = 7 - current
      
      self.periods[periodsIncompleted[0]]['completed'] = True

      periodEtcC = cropData['kc'][periodsIncompleted[0]] * et0 * current
      periodEtcN = cropData['kc'][periodsIncompleted[1]] * et0 * nextDays



  def incompletedPeriods(self):
    periods = []
    for e in self.periods:
      if not e['completed']:
        periods.append(e)

    return periods

def createUser(id, username, password):
  newUser = User(id, username, password)

  return newUser

def littersQuantity(missing, area, irrigationType):
  litters = missing * area
  addition = 0
  
  if irrigationType == 'Aspersión':
    addition = 0.30
  elif irrigationType == 'Microaspersión':
    addition = 0.15
  
  litters = litters + (litters * addition)

  return litters

def irrigationCapacity(area):
  irrigation = area / 36
  littersCapacity = irrigation * 1000

  return littersCapacity

def littersPerMinute(irrigationQuantity, needs):
  results = 1

  if irrigationQuantity > needs:
    results = irrigationQuantity % needs
  elif irrigationQuantity < needs:
    results = needs % irrigationQuantity
  
  return results

def leftOverRain(key, obj):
  before = ''
  for e in obj.keys():
    if before == key:
      obj[e]['rain'] -= obj[key]['missing']
      return obj
    before = e
  return obj
