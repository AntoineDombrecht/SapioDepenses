import unidecode
import numpy as np
from datetime import datetime

class Utils:
    def __init__(self, val = None):
        self.val = val

    def normalize(self, val):
        value = unidecode.unidecode(val).upper()
        value = value.replace('#', '')
        
        return value
    
    def listEven (self, max) :
        result = []
        for x in range(0,max) :
            if x % 2 == 0 :
                result.append(x)
        return result
    
    def is_above(self, p, a, b) :
        return np.cross(p-a, b-a) < 0
        
        
   