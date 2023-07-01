from datetime import datetime
from datetime import timedelta
import pytz

# Logs
DEBUG = False
DEBUG_LVL = 9

# Mongo
HOST = 'mongodb://localhost:27017'
DELAY = 3000
DATABASE = 'depenses'
COMPTE_COURANT = 'compte.courant'
COMPTE_EPARGNE = 'compte.epargne'

# Horodatage
HEURE_ETE = 2
HEURE_HIVERS = 1
HEURE = HEURE_ETE
DATE_TIME_PATERN = '%d/%m/%Y %H:%M:%S'
DATE_PATERN = '%d/%m/%Y'
MOIS = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']

# Fonds initiaux
FOND_COMPTE_COURANT = 1000
FOND_COMPTE_EPARGNE = 1000

# Analyse
ECHELLE = 'JOUR'
VISION  = 'MOIS'
VALEUR_MOIS  = 10
VALEUR_ANNEE  = 2022
DOSSIER = '30-09-2022'
FICHIER = 'Releve_compte_30_09_2022.csv'

# Compte Courant
# Arbre
CAT_2  = 'ENTREE'
CAT_3  = 'SORTIE'
CAT_4  = 'SALAIRE'
CAT_5  = 'ENERGIE'
CAT_6  = 'ALIMENTAIRE'
CAT_7  = 'ASSURANCE'
CAT_8  = 'ETAT'
CAT_9  = 'COURSES'
CAT_10 = 'RESTAURANT'
# Chemins
CAT_1             = CAT_2, CAT_3
CAT_1_CAT_2       = CAT_4,
CAT_1_CAT_3       = CAT_5, CAT_6, CAT_7, CAT_8
CAT_1_CAT_3_CAT_6 = CAT_9, CAT_10

#Compte Epargne
# Arbre
CAT_B  = 'ENTREE'
CAT_C  = 'SORTIE'
CAT_D  = 'TRAVAUX'
CAT_E  = 'ENFANTS'
CAT_F  = 'PARENTS'
CAT_G  = 'RETRAITE'
# Chemins
CAT_A = CAT_B, CAT_C
CAT_C = CAT_D, CAT_E, CAT_F, CAT_G

#IMPORTANCE DES PROJETS DE VIE
TRAVAUX_POURCENTAGE  = 25    / 100
ENFANTS_POURCENTAGE  = 25    / 100
PARENTS_POURCENTAGE  = 25    / 100
RETRAITE_POURCENTAGE = 25    / 100

# Widgets
VALIDER = 'VALIDER'
MONTANT = 'MONTANT'
DESCRIPTION = 'DESCRIPTION'
OCCURRENCE = 'OCCURENCE'
OPTIONS = ['AUCUNE', 'JOUR', 'SEMAINE', 'MOIS', "BIMENSUEL", 'ANNEE']
CONTEXTE = 'CONTEXTE'
DATE = 'DATE'

# Diagramme
ZOOM       = 25/100
RESOLUTION = 200
LIMITE     = 1000
INF        = 10000000000