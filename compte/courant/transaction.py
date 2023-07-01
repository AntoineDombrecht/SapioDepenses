from constant import *
from database import Database
from requete import Requete
from compte.courant.entite import Entite
from date import Date
from math import *

class Transaction:
  def __init__(self):
    self.database =  Database()
    self.database.setCollection(COMPTE_COURANT)
    
  def deleteAll(self):
    self.database.setInstruction(
        Requete().all()
    )
    self.database.delete()
    
  def initialize(self):
    entite = Entite()
    
    date = Date().now.replace(day=1)
    date = date.replace(month=1)
    date = date.replace(year=2000)
    
    entite.setDate(date)
    entite.fond = FOND_COMPTE_COURANT
    entite.fondTotal = FOND_COMPTE_COURANT
    entite.mouvement = FOND_COMPTE_COURANT
    entite.mouvementJournalier = FOND_COMPTE_COURANT
    entite.mouvementHebdomadaire= FOND_COMPTE_COURANT
    entite.mouvementMensuel = FOND_COMPTE_COURANT
    
    entite.type = ENTREE
    entite.montant = FOND_COMPTE_COURANT
    entite.contexte = None
    entite.description = None
    entite.occurrence = None
    
    entite.roundAll()
    self.database.setEntities(vars(entite))
    self.database.write()
    
  def save(self, entite):  
    last       = self.readLastUntil(entite.date)    
    dayUntil   = self.readDayUntil(entite.date)    
    weekUntil  = self.readWeekUntil(entite.date)    
    monthUntil = self.readMonthUntil(entite.date)
    
    entite.mouvement = entite.montant if ENTREE in entite.type else -entite.montant
    
    entite.fond =      last['fond']      + entite.mouvement
    entite.fondTotal = last['fondTotal'] +  entite.mouvement if ENTREE in entite.type else last['fondTotal']
        
    entite.mouvementJournalier =   sum(t['mouvement'] for t in dayUntil)   + entite.mouvement
    entite.mouvementHebdomadaire = sum(t['mouvement'] for t in weekUntil)  + entite.mouvement
    entite.mouvementMensuel =      sum(t['mouvement'] for t in monthUntil) + entite.mouvement
    
    entite.roundAll()
    self.database.setEntities(vars(entite))
    self.database.write()
    
    self.incrementAllAfter(entite)    

  def readAll(self):
    self.database.setInstruction(
        Requete().all()
    )
    return self.database.read()
    
  def incrementAllAfter(self, entite):
    self.database.setInstruction(Requete().allAfter(entite.date))
    if ENTREE in entite.type :
        self.database.increment('fondTotal',entite.mouvement)
    
    self.database.setInstruction(Requete().allAfter(entite.date))
    self.database.increment('fond',entite.mouvement)
    
    self.database.setInstruction(Requete().dayAfter(entite.date))
    self.database.increment('mouvementJournalier',entite.fond)
    
    self.database.setInstruction(Requete().weekAfter(entite.date))
    self.database.increment('mouvementHebdomadaire',entite.fond)
    
    self.database.setInstruction(Requete().monthAfter(entite.date))
    self.database.increment('mouvementMensuel',entite.fond)
    
  def totalSortie (self, recherche) :    
    self.database.setInstruction(
        Requete().expenses_regex(recherche)
    )
    data = self.database.read()
    return abs(ceil(sum(list([ x['mouvement'] for x in data]))/9.0))
  
  def readLastUntil(self, date):
    self.database.setInstruction(
        Requete().lastUntil(date)
    )
    return self.database.read()[0]
    
  def readDayUntil(self, date):
    self.database.setInstruction(
        Requete().dayUntil(date)
    )
    return self.database.read()
  
  def readDayAfter(self, date):
    self.database.setInstruction(
        Requete().dayAfter(date)
    )
    return self.database.read()
    
  def readWeekUntil(self, date):
    self.database.setInstruction(
        Requete().weekUntil(date)
    )
    return self.database.read()
  
  def readWeekAfter(self, date):
    self.database.setInstruction(
        Requete().weekAfter(date)
    )
    return self.database.read()
  
  def readMonthAfter(self, date):
    self.database.setInstruction(
        Requete().monthAfter(date)
    )
    return self.database.read()
    
  def readMonthUntil(self, date):
    self.database.setInstruction(
        Requete().monthUntil(date)
    )
    return self.database.read()
    
