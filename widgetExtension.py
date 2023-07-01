from constant import *
import ipywidgets as w
from compte.courant.transaction import Transaction as CompteCourant
from compte.courant.entite import Entite
from utils import Utils
from date import Date

class widgetExtension:
    def __init__(self, options, parent, parentOption, show = False):
        self.options = options
        self.widget = w.Dropdown(options=self.options)
        self.parent = parent
        self.parentOption = parentOption
        self.children = []
        self.box = w.VBox()
        self.show() if show else self.hide()
        self.widget.observe(self.onChange)
        self.type = ''
        self.montant = w.FloatText(description=MONTANT)
        self.description = w.Text(description=DESCRIPTION)
        self.contexte = w.Text(description=CONTEXTE)
        self.occurrence = w.SelectionSlider(options=OPTIONS,description=OCCURRENCE)
        self.date = w.DatetimePicker(description=DATE, disabled=False)
        self.button = w.Button(description=VALIDER)
        self.out = w.Output()
        self.styling()
        
    def styling(self) : 
        self.widget.layout.margin = '0 0 0 0'
        self.box.layout.margin = '0 0 0 0'
        self.button.layout.display='flex'
        self.button.layout.flex_flow='column'
        self.button.layout.align_items='center'
        self.button.layout.width='300px'
        self.widget.style.description_width='82px'
        
    def addMontant(self):
        self.box.children += tuple([self.montant])
                
    def addDescription(self):
        self.box.children += tuple([self.description])
        
    def addContexte(self):
        self.box.children += tuple([self.contexte])
    
    def addOccurrence(self):
        self.box.children += tuple([self.occurrence])
        
    def addDate(self):
        self.date.value = Date().now - timedelta(hours=HEURE)
        self.box.children += tuple([self.date])
    
    def addButton(self):
        self.box.children += tuple([self.button])
        self.button.on_click(self.save)
        
    def addOutput(self):
        self.box.children += tuple([self.out])
    
    def addType(self):
        self.box.children += tuple([self.widget])
        
        if(self.children):
            for child in self.children:
                self.box.children += tuple([child.addType()])
        return self.box

    def onChange(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            for option in self.widget.options:
                #Enfant selectionné
                if(self.widget.value == option):
                    for child in self.children:
                        #On affiche cet enfant
                        if(child.parentOption == option):
                            child.show()
                        #Et on masque les autres enfants
                        else:
                            child.hide()
    
    def hide(self):
        self.widget.layout.visibility = 'hidden'
        self.widget.layout.height = '0px'
        self.widget.value = None
        self.hideDescendance()

    def show(self):
        self.widget.layout.visibility = 'visible'
        self.widget.layout.height = 'inherit'
        self.widget.layout.justify_content = 'space-around'
        self.widget.value = None
        
    def hideDescendance(self):
        if(self.children):
            for child in self.children:
                child.hide()
                
    def showDescendance(self):
        if(self.children):
            for child in self.children:
                child.show()
                
    # Retourne la liste concaténée de tous les types
    def getAllValues(self):
        value = self.widget.value+' ' if self.widget.value else ''
                
        if(self.children):
            for child in self.children:
                value += child.getAllValues()
        return value;
    
    def save(self, b):
        entite = Entite()
        entite.type = self.getAllValues()
        entite.montant = self.montant.value
        entite.date = self.date.value
        entite.occurrence = self.occurrence.value
        entite.contexte = Utils().normalize(self.contexte.value)
        entite.description =  Utils().normalize(self.description.value)
        
        CompteCourant().save(entite)                