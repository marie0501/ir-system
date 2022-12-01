from src.boolean_model import Boolean
from src.collection import Cranfield
from src.vectorial_model import Vectorial
import time
import numpy as np

a = np.array([[1,2,3],[4,5,6]])
print(a.shape)
print(1/6)

model = Vectorial()
collection = Cranfield('C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\cran\\cran.all.1400')
query = '(stream and layer) or aerodynamics.'
start = time.time()
print(model.search(query, collection,'cranfield_indexed_terms','cranfield_max_freq'))
end = time.time()
print(end-start)