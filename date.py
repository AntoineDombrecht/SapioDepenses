from datetime import datetime
import calendar
from constant import *

class Date:
   def __init__(_):
    _.now = datetime.now(pytz.utc) + timedelta(hours=HEURE)
    
    _.currentMonth = _.now.month
    _.currentDay = datetime.now().day
    _.currentWeek  = _.now.isocalendar()[1]
    _.currentYear  = _.now.year    
    
    _.lastYear  = _.currentYear - 1
    _.lastMonth = _.currentMonth - 1 if _.currentMonth > 1 else 12
    _.lastWeek  = _.currentWeek  - 1 if _.currentWeek  > 1 else _.now.replace(day=31, month=12,  year=_.lastYear).isocalendar()[1]
    
   def finalMonth(_, number):
    actualMonth = _.currentMonth
    finalMonth = actualMonth + number
    while actualMonth != finalMonth:
        actualMonth = actualMonth+1 if actualMonth < 12 else 1
    return actualMonth
    
   def listeMois(_, custom, final) :
    return MOIS[custom-1 : final-1]
    
   def floatToDateTime(self, value):
    if(isinstance(value, datetime)):
        return value
    if(isinstance(value, float)):
        return datetime.fromtimestamp(value)
    
   def toString(_, date):
    return date.strftime(DATE_PATERN)
  
   def toDateTime(_, date, format):
    return datetime.strptime(date, format)
  
   def toTimestamp(_):
    return _.valeur.timestamp() 
    
   def dayMonthFrom(_, date):
    return int(date.strftime("%d"))
    
   def monthFrom(_, date):
    return date.month
  
   def yearFrom(_, date):
    return date.year
  
   def weekFrom(_, date):
    return date.isocalendar()[1]
    
   def dayWeekFrom(_, date):
    return date.weekday()
    
   def dayYearFrom(_, date):
    return int(date.strftime('%j'))
    
   def nbDayFromMonth(_, month, year):
        return calendar.monthrange(year, month)[1]