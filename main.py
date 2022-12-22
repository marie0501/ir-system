from ir_app.src.boolean_model import Boolean
from ir_app.src.collection import Cranfield, Scifact
from ir_app.src.vectorial_model import Vectorial
from ir_app.src.lsi_model import LSI
from ir_app.src.tester import Tester
import time
import numpy as np
import pickle

import matplotlib.pyplot as plt


model = {'boolean': Boolean(), 'vectorial': Vectorial(), 'lsi':LSI()}        
collection = {'cranfield': Cranfield('C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\cran'), 'scifact': Scifact("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\scifact") }

def parse(collection, documents_filename):
    collection.parse_documents(documents_filename)

def retrieve(user_query, user_collection, user_model):

    irm = model[user_model]
    coll = collection[user_collection]
    docs = irm.search(user_query, coll)
           
    file_name = 'retrieved_documents'

    with open(file_name,'wb') as f:
        pickle.dump(docs, f, protocol=pickle.HIGHEST_PROTOCOL)
      



