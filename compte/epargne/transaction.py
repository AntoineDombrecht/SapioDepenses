from constant import *
from database import Database
from requete import Requete
from compte.epargne.entite import Entite
from compte.courant.entite import Entite as EntiteCompteCourant
from compte.courant.transaction import Transaction as CompteCourant
from date import Date

class Transaction:
  def __init__(self):
    self.database =  Database()
    self.database.setCollection(COMPTE_EPARGNE)
    
  def deleteAll(self):
    self.database.setInstruction(
        Requete().all()
    )
    self.database.delete()
    
  def initialize(self):
    entite = Entite()
    
    entite.type = ENTREE
    entite.montant = FOND_COMPTE_EPARGNE
    entite.contexte = None
    entite.description = None
    entite.occurrence = None
    
    entite.setDate(Date().now.replace(day=1))
    entite.fond = FOND_COMPTE_EPARGNE
    entite.fondTotal = FOND_COMPTE_EPARGNE
    entite.mouvement = FOND_COMPTE_EPARGNE
    entite.mouvementJournalier = FOND_COMPTE_EPARGNE
    entite.mouvementHebdomadaire= FOND_COMPTE_EPARGNE
    entite.mouvementMensuel = FOND_COMPTE_EPARGNE
    
    entite.type = ENTREE
    entite.montant = FOND_COMPTE_EPARGNE
    entite.contexte = None
    entite.description = None
    entite.occurrence = None
    
    entite.fondTravaux = entite.fondTotal*TRAVAUX_POURCENTAGE
    entite.fondEnfants = entite.fondTotal*ENFANTS_POURCENTAGE
    entite.fondParents = entite.fondTotal*PARENTS_POURCENTAGE
    entite.fondRetraite = entite.fondTotal*RETRAITE_POURCENTAGE
    
    entite.roundAll()
    self.database.setEntities(vars(entite))
    self.database.write()
    
  def save(self, entite):  
    last = self.readLastUntil(entite.date)        
    dayUntil = self.readDayUntil(entite.date)    
    weekUntil = self.readWeekUntil(entite.date)    
    monthUntil = self.readMonthUntil(entite.date)
    
    entite.mouvement = entite.montant if ENTREE in entite.type else -entite.montant
    
    entite.fond =      last['fond']      +  entite.mouvement
    entite.fondTotal = last['fondTotal'] +  entite.mouvement if ENTREE in entite.type else last['fondTotal']  
    
    entite.mouvementJournalier =   sum(t['mouvement'] for t in dayUntil)   + entite.mouvement
    entite.mouvementHebdomadaire = sum(t['mouvement'] for t in weekUntil)  + entite.mouvement
    entite.mouvementMensuel =      sum(t['mouvement'] for t in monthUntil) + entite.mouvement
    
    entite.fondTravaux =          last['fondTravaux']      
    entite.fondEnfants =          last['fondEnfants']     
    entite.fondParents =          last['fondParents']       
    entite.fondRetraite =         last['fondRetraite']      
    
    if ENTREE in entite.type :
        entite.fondTravaux += entite.mouvement*TRAVAUX_POURCENTAGE
        entite.fondEnfants += entite.mouvement*ENFANTS_POURCENTAGE
        entite.fondParents +=  entite.mouvement*PARENTS_POURCENTAGE
        entite.fondRetraite += entite.mouvement*RETRAITE_POURCENTAGE
        
    else :
        if TRAVAUX in entite.type :
            entite.fondTravaux += entite.mouvement
        if ENFANTS in entite.type :
            entite.fondEnfants += entite.mouvement
        if PARENTS in entite.type :
            entite.fondParents +=  entite.mouvement
        if RETRAITE in entite.type :
            entite.fondRetraite += entite.mouvement
    
    entite.roundAll()
    self.database.setEntities(vars(entite))
    self.database.write()
    
    self.incrementAllAfter(entite)
    
    entite_ = EntiteCompteCourant()
    entite_.type = entite.type.replace(ENTREE,SORTIE) if ENTREE in entite.type else entite.type.replace(SORTIE,ENTREE)
    entite_.montant = entite.montant
    entite_.date = entite.date
    entite_.contexte = entite.contexte
    entite_.occurrence = entite.occurrence
    entite_.description = entite.description
    entite_.setDate(entite_.date)
    
    CompteCourant().save(entite_)
  def readAll(self):
    self.database.setInstruction(
        Requete().all()
    )
    return self.database.read()
    
  def incrementAllAfter(self, entite):
    self.database.setInstruction(Requete().allAfter(entite.date))
    
    if ENTREE in entite.type :
        self.database.increment('fondTotal',entite.mouvement)
        self.database.increment('fondTravaux',entite.mouvement*TRAVAUX_POURCENTAGE)
        self.database.increment('fondEnfants',entite.mouvement*ENFANTS_POURCENTAGE)
        self.database.increment('fondParents',entite.mouvement*PARENTS_POURCENTAGE)
        self.database.increment('fondRetraite',entite.mouvement*RETRAITE_POURCENTAGE)
    else :
        if TRAVAUX in entite.type :
            self.database.increment('fondTravaux',entite.mouvement)
        if ENFANTS in entite.type :
            self.database.increment('fondEnfants',entite.mouvement)
        if PARENTS in entite.type :
            self.database.increment('fondParents',entite.mouvement)
        if RETRAITE in entite.type:
            self.database.increment('fondRetraite',entite.mouvement)
    
    self.database.setInstruction(Requete().allAfter(entite.date))
    self.database.increment('fond',entite.mouvement)
    
    self.database.setInstruction(Requete().allAfter(entite.date))
    self.database.increment('fond',entite.mouvement)
    
    self.database.setInstruction(Requete().dayAfter(entite.date))
    self.database.increment('mouvementJournalier',entite.fond)
    
    self.database.setInstruction(Requete().weekAfter(entite.date))
    self.database.increment('mouvementHebdomadaire',entite.fond)
    
    self.database.setInstruction(Requete().monthAfter(entite.date))
    self.database.increment('mouvementMensuel',entite.fond)
    
    
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