from date import Date

class Entite:
  def __init__(self):
    self.type = None
    self.montant = None
    self.contexte = None
    self.description = None
    self.occurrence = None
    
    self.fond = None
    self.fondTotal = None
    
    self.mouvement = None
    self.mouvementJournalier = None
    self.mouvementHebdomadaire = None
    self.mouvementMensuel = None
    
    self.date = None
    self.jourSemaine = None
    self.semaine = None
    self.jourMois = None
    self.mois = None
    self.annee = None
    self.jourAnnee = None
    
  def roundAll(self):
    self.montant = round(self.montant,2)
    
    self.fond = round(self.fond,2)
    self.fondTotal = round(self.fondTotal,2)
    
    self.mouvement = round(self.mouvement,2)
    self.mouvementJournalier = round(self.mouvementJournalier,2)
    self.mouvementHebdomadaire = round(self.mouvementHebdomadaire,2)
    self.mouvementMensuel = round(self.mouvementMensuel,2)
    
  def setDate(self, date):
    self.date = date
    self.jourSemaine = Date().dayWeekFrom(date)
    self.semaine = Date().weekFrom(date)
    self.jourMois = Date().dayMonthFrom(date)
    self.mois = Date().monthFrom(date)
    self.annee = Date().yearFrom(date)
    self.jourAnnee = Date().dayYearFrom(date)