from constant import *
from datetime import datetime, timedelta
from date import Date

class Requete:
  def __init__(self) :
    self.match   = {}
    self.sort    = {"date":-1}
    self.limit = INF
    
  def all(self) :
    return self
    
  def lastUntil(self, date) :
    self.limit = 1
        
    if date is not None:
        self.match = {
            'date' : { "$lte": date}
        }
        
    return self
  
  def allAfter(self, date) :
    self.match = {
        'date' : { "$gt": date}
    }
    return self
  
  def currentDay(self) :
    self.match = {
        'jourMois' : {
            "$eq": Date().currentDay
        },
        'mois' : {
            "$eq": Date().currentMonth
        },
        'annee' : {
            "$eq": Date().currentYear
        }
    }
    return self
    
  def dayUntil(self, date) :    
    self.match = {
        'date' : { 
            "$lte": date
        },
        'jourMois' : {
            "$eq": Date().dayMonthFrom(date)
        },
        'mois' : {
            "$eq": Date().monthFrom(date)
        },
        'annee' : {
            "$eq": Date().yearFrom(date)
        }
    }
    return self
  
  def dayAfter(self, date) :
    self.match = {
        'date' : { 
            "$gt": date
        },
        'jourMois' : {
            "$eq": Date().dayMonthFrom(date)
        },
        'mois' : {
            "$eq": Date().monthFrom(date)
        },
        'annee' : {
            "$eq": Date().yearFrom(date)
        }
    }
    return self
  
  def currentMonth(self) :
    self.match = {
        'mois' : {
            "$eq": Date().currentMonth
        },
        'annee' : {
            "$eq": Date().currentYear
        }
    }
    return self
    
  def monthUntil(self, date) :
    self.match = {
        'date' : { 
            "$lte": date
        },
        'mois' : {
            "$eq": Date().monthFrom(date)
        },
        'annee' : {
            "$eq": Date().yearFrom(date)
        }
    }
    return self
    
  def monthAfter(self, date) :    
    self.match = {
        'date' : { 
            "$gt": date
        },
        'mois' : {
            "$eq": Date().monthFrom(date)
        },
        'annee' : {
            "$eq": Date().yearFrom(date)
        }
    }
    return self
    
  def weekUntil(self, date) :
    self.match = {
        'date' : { 
            "$lte": date
        },
        'semaine' : {
            "$eq": Date().weekFrom(date)
        },
        'mois' : {
            "$eq": Date().monthFrom(date)
        },
        'annee' : {
            "$eq": Date().yearFrom(date)
        }
    }
    return self
  
  def weekAfter(self, date) :
    self.match = {
        'date' : { 
            "$gt": date
        },
        'semaine' : {
            "$eq": Date().weekFrom(date)
        },
        'mois' : {
            "$eq": Date().monthFrom(date)
        },
        'annee' : {
            "$eq": Date().yearFrom(date)
        }
    }
    return self
  
  def currentWeek(self) :
        
    self.match = {
        'semaine' : {
            "$eq": Date().currentWeek
        },
        'mois' : {
            "$eq": Date().currentMonth
        },
        'annee' : {
            "$eq": Date().currentYear
        }
    }
    return self
  
  def expenses_regex(self,recherche):
    array = []
    for rech in recherche :
        mot = rech['mot']
        colonne = rech['colonne'] 
        array.append({ colonne : { "$regex" : '^.*'+mot+'.*$' }})
    self.match = {"$and" : array}
    return self