from src.boolean_model import Boolean
from src.collection import Cranfield
from src.vectorial_model import Vectorial
from src.lsi_model import LSI
import time
import numpy as np
import pickle

#a = np.array([])
#print(a.shape)
#np.append(a,[1,2,3])
#print(a)
#print(1/6)
model = {'boolean': Boolean(), 'vectorial': Vectorial(), 'lsi':LSI()}        
collection = {'cranfield': Cranfield('C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\cran\\cran.all.1400')}

def retrieve(user_query, user_collection, user_model):
    irm = model[user_model]
    coll = collection[user_collection]
    docs = irm.search(user_query, coll,'cranfield_indexed_terms')
    file_name = 'retrieved_documents'
    with open(file_name,'wb') as f:
        pickle.dump(docs, f, protocol=pickle.HIGHEST_PROTOCOL)
        
    print('ok')
    return file_name


#model = Boolean()
#collection = Cranfield('C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\cran\\cran.all.1400')
#query = '(stream and layer) or aerodynamics.'
#start = time.time()
#print(model.search(query, collection,'cranfield_indexed_terms'))
#end = time.time()
#print(end-start)