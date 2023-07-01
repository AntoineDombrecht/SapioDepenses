import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as patches
import numpy as np
import math 

from constant import *
from date import Date
from utils import Utils
from compte.courant.transaction import Transaction as CompteCourant
from compte.courant.entite import Entite

class Diagram:
   def __init__(self):        
    
    # Données
    self.maxJours    = Date().nbDayFromMonth(VALEUR_MOIS, VALEUR_ANNEE)
    self.depenses    = self.miseEnForme()
    self.length      = len(self.depenses)
    self.totaux      = list([ x['total'] for x in self.depenses ])
    self.totauxEgaux = self.checkAllIdentical()
    self.maxTotaux   = max(self.totaux)
    self.minTotaux   = min(self.totaux)
    self.totalRestant= self.totaux[-1]
    self.jours       = list([ y['jour'] for y in self.depenses ])
    self.montants    = list([ z['montant'] for z in self.depenses ]) 
    self.sumMontant  = sum(self.montants)
    self.hauteur     = self.maxTotaux + 200
    self.bas         = 0 if self.minTotaux > 0 else self.minTotaux - 200
    
    #Initialisation
    self.fig  = plt.figure(figsize=(self.maxJours, 10), dpi=RESOLUTION)
    self.ax   = self.fig.add_subplot()
    
   def fonctionDemarcation(self, x, l=True):
    a = -(self.totaux[0]-LIMITE)/self.maxJours
    b = self.totaux[0]-a
    return (a*x)+b if l else (x-b)/a
    
   def afficherLegende(self):
    
    legend_elements = [
                        patches.Rectangle((0,0),0,0, color='green', label='Marge permise'),
                        Line2D([0], [0], color='blue', lw=2, label='Tendance'),
                        Line2D([0], [0], color='red', lw=2, linestyle='--', label='Épargne Prévue'),
                      ]
    
    self.ax.legend(handles=legend_elements, prop={'size': 25}, loc='upper right')
    
    depensesActuelle = round(self.sumMontant / self.maxJours)
    depensesCiblee   = round((self.totaux[0] - LIMITE )/ self.maxJours)
    nbJoursSansDepense = 0
    nbJoursAvecDepense = 0
    
    for depense in self.montants :
        if depense == 0 :
            nbJoursSansDepense+=1
        else :
            nbJoursAvecDepense+=1
    
    info1    =  'Dépenses autorisées  :  ' + str(depensesCiblee)     + ' € / jour \n'
    info2    =  'Dépenses actuelle    :  ' + str(depensesActuelle)   + ' € / jour \n'
    info3    =  'Jours sans dépense   :  ' + str(nbJoursSansDepense) + '\n'
    info4    =  'Jours avec dépense   :  ' + str(nbJoursAvecDepense) + '\n'
    self.ax.text(1.5, LIMITE-600, info1 + info2 + info3 + info4, fontsize = 20)
        
   def afficherTendance(self):
    x1 = 1
    y1 = self.totaux[0]
    x2 = self.fonctionTendance(LIMITE, False)
    y2 = self.fonctionTendance(x2)
    y3 = self.fonctionTendance(self.maxJours)
    x3 = self.fonctionTendance(y3, False)
    
    # Epargne à y = LIMITE
    self.ax.plot([x1,x2], [y1, y2], 'b-', alpha=0.2, label='Tendance',linewidth=3)
    self.ax.annotate(round(x2), (x2+0.25, 50), weight = "bold", fontsize=15)
    self.ax.plot([x2,x2], [LIMITE, 0], 'b--', alpha=0.2, markersize=10, label='Tendance',linewidth=3)
    
    # Epargne à x = fin de la periode
    self.ax.plot([x2,x3], [y2, y3], 'r-', alpha=0.2, label='Tendance',linewidth=3)
    self.ax.plot([0,self.maxJours], [y3, y3], 'r--', alpha=0.2, markersize=10, label='Tendance',linewidth=3)
    self.addValueOnSecondYAxis(y3)
    
   def addValueOnSecondYAxis(self,y3) :
    ax2  = self.ax.twinx()
    ax2.set_ylim(0, self.hauteur)
    ax2.set_yticks(list([y3]))
    ax2.tick_params(axis='y', which='major', labelsize=20)
    ax2.set_ylabel('Euros', fontsize=20)
    
   def afficherDemarcation(self):
    x1 = 0
    y1 = self.fonctionDemarcation(x1)
    y2 = LIMITE
    x2 = self.fonctionDemarcation(y2, False)
    
    plt.fill_between([x1,x2], [self.hauteur,self.hauteur], color='green', alpha=0.08)
    plt.fill_between([x1,x2], [y1, y2], color='white')
    plt.fill_between([x1,x2], [y1, y2], color='red', alpha=0.08)
    plt.fill_between([x1,x2], [LIMITE, LIMITE], color='white')
    
   def afficherIntervalle(self):
    x1 = 0
    y1 = self.fonctionDemarcation(x1)
    y2 = LIMITE
    x2 = self.fonctionDemarcation(y2, False)
    
    a = np.array([x1,y1])
    b = np.array([x2,y2])
    
    montant = self.montants[2]
    
    for i in range(2):
        p1 = np.array([i,montant])

        if Utils().is_above(p1,a,b):
            self.ax.scatter(p1[0], p1[1], color='green')
        else:
            self.ax.scatter(p1[0], p1[1], color='red')
    
   def afficherValeursDepenses(self):
    for i in range(0, self.length) :
        if (self.totaux[i-1] != self.totaux[i]) :
            self.ax.annotate(
                round(self.montants[i]), 
                (self.jours[i], self.totaux[i]), 
                (self.jours[i], self.totaux[i]+35), 
                weight = "bold", 
                fontsize=15
            )
       
   def afficherLimite(self) :
    self.ax.axhline(LIMITE, color = 'r', linestyle = '-', label='Limite',linewidth=3, alpha=0.2)
    
   def afficherCoordonnees(self) :
    # Ajout axes    
    self.ax.set_ylim(self.bas, self.hauteur)
    self.ax.set_xlim(0, self.maxJours)
    
    # Ajout intervalles
    self.ax.set_xticks(self.jours, self.jours)
    self.ax.set_yticks(np.arange(0, self.hauteur, 200))
    self.ax.tick_params(axis='both', which='major', labelsize=20)
    
    # Ajout grille
    plt.grid(which='both')
    plt.grid(which='major', alpha=0.5)
    
    # Ajout légende
    self.ax.set_title('Dépenses sur le mois', fontsize=20)
    self.ax.set_xlabel('Jours', fontsize=20)
    self.ax.set_ylabel('Euros', fontsize=20)
    
   def afficherNuage(self):    
    for i in range(0,self.length) :
        if(self.totaux[i] != self.totaux[i-1] and self.totaux[i] >= LIMITE):
            color = 'orange'
        elif (self.totaux[i] == self.totaux[i-1]):
            color = 'green'
        elif(self.totaux[i] != self.totaux[i-1] and self.totaux[i] <= LIMITE):
            color = 'red'
            
        self.ax.plot(self.jours[i], self.totaux[i], 'o', color=color, markersize=10)  
    
   def sauvegarder(self):
    chemin  = 'img/depense '+ str(VALEUR_MOIS) + '-'  
    chemin +=  str(VALEUR_ANNEE) +'.png'
    self.fig.savefig(chemin, dpi=200)
    
   def fonctionTendance(self, k, l=True):
    total = self.length
    
    moyenne_y = sum(self.totaux) / total
    moyenne_x = sum(self.jours) / total
    
    # Calcul de la variance de X
    calcul = 0

    for x in self.jours :
        calcul += ( x - moyenne_x )**2
    variance_x = ( 1/total ) * calcul
    
    # Calcul de la covariance X,Y
    calcul=0
    for i in range(total) :
        calcul += ( self.jours[i] * self.totaux[i] ) - ( moyenne_x * moyenne_y )

    covariance_xy = ( 1/total ) * calcul
    
    # Calcul des coefficients a et b
    a = covariance_xy / variance_x
    b = moyenne_y - ( a * moyenne_x )
    return (a*k)+b if l else (k-b)/a
    
   def miseEnForme(self):  
        resultats = []
        
        for jour in range(1,self.maxJours):
            date = Date().now.replace(day=jour)
            date = date.replace(month=VALEUR_MOIS)
            date = date.replace(year=VALEUR_ANNEE)
            data  = CompteCourant().readLastUntil(date)
            resultat =  {
                'jour': jour, 
                'montant':data['mouvementJournalier'], 
                'total':data['fond']
            }
            resultats.append(resultat)
        return resultats

   def checkAllIdentical(self):
    for total in self.totaux :
        if total != self.totaux[0]:
            return False
    return True