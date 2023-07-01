from constant import *
import pymongo

class Database:
  def __init__(self):
    self.db = self.getDatabase()
    self.collection = None
    self.instruction = None
    self.entities = []
    
  def getDatabase(self):
    try:
        client = pymongo.MongoClient(HOST, serverSelectionTimeoutMS=DELAY)
        client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        return None
    return client[DATABASE]
  
  def getCollection(self, compte):
    if self.db is not None:
        return self.db[compte]
    else:
        return None
    
  def setCollection(self, collection):
    match collection:
        case 'compte.courant':
            self.collection = self.getCollection(COMPTE_COURANT)
        case 'compte.epargne':
            self.collection = self.getCollection(COMPTE_EPARGNE)
            
  def setInstruction(self, requete):     
    
    pipeline = [
        { "$match"    : requete.match   },
        { "$sort"     : requete.sort    },
        { "$limit"    : requete.limit   }
    ]    
    
    self.instruction = self.collection.aggregate(pipeline)
    
  def resetInstruction(self):
    self.instruction = None
    
  def setEntities(self, entities):     
    self.entities.append(entities)  
    
  def delete(self):        
    result = []
    for data in self.instruction:
        result.append(data['_id'])
    
    self.collection.delete_many({'_id':{'$in':result}})
    
  def read(self):        
    result = []
    for data in self.instruction:
        result.append(data)
    self.resetInstruction()
    return result
    
  def write(self):
    return self.collection.insert_many(self.entities)
    
  def update(self, colonne, valeur):  
    result = []
    for data in self.instruction:
        result.append(data['_id'])
    
    self.collection.update_many(
        {'_id':{'$in':result}},
        {"$set": {'occurrence': 'MOIS'}}
    )
    
  def increment(self, colonne, value):
    result = []
    for data in self.instruction:
        result.append(data['_id'])
    
    self.collection.update_many(
        {'_id':{'$in':result}},
        {"$inc": {colonne: value}}
    )