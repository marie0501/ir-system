import numpy as np
import random
from .vectorial_model import Vectorial
from numpy.linalg import svd, inv
#from scipy.linalg import svd
#from scipy.sparse.linalg import svds

class LSI(Vectorial): 

    def __init__(self):
        self.name = "lsi"   
    
    def search(self, query, collection):        
        
        k=200
        term_document_matrix = self._get_matrix(collection)
        indexed_terms = self._load(collection.name + '\\' + collection.name + '_indexed_terms')
        idf_matrix = self._load(collection.name + '\\' + collection.name + '_idf_matrix')
        U_k,S_k,Vt_k = self.__low_rank_approximation(term_document_matrix,collection,k)
        query_vector = self._process_query(query, indexed_terms, idf_matrix, 0.5)
        query_k = self.__query_low_rank_approx(query_vector,U_k,S_k)
        retrieved_documents_similarity = self._similarity(Vt_k, query_k)

        self._save(retrieved_documents_similarity,self.name + '_retrieved_documents_similarity')

        return collection.retrieve_documents(retrieved_documents_similarity)

    def __low_rank_approximation(self, term_document_matrix, collection , k):
        
        U_k = self._load(collection.name + '\\' + collection.name + '_U_k_'+ str(k))

        if len(U_k) > 1:            
            Vt_k = self._load(collection.name + '\\' + collection.name + '_Vt_k_'+ str(k))
            S_k = self._load(collection.name + '\\' + collection.name + '_S_k_'+ str(k))
            return U_k, S_k, Vt_k

        else:
            U,S,Vt = svd(term_document_matrix)
            S_k = np.zeros((k,k))

            for i in range(k):
                S_k[i,i]=S[i]

            U_k=U[:,:k]                  
            Vt_k=Vt[:k,:]

            self._save(U_k, collection.name + '\\' + collection.name + '_U_k_'+ str(k))
            self._save(S_k, collection.name + '\\' + collection.name + '_S_k_'+ str(k))
            self._save(Vt_k, collection.name + '\\' + collection.name + '_Vt_k_'+ str(k))

            return U_k, S_k, Vt_k 

        
    #reducir la dimesion del vector consuta 
    def __query_low_rank_approx(self,query_vector, U_k, S_k):

        Ut_k = np.transpose(U_k)

        return np.matmul(np.matmul(S_k,Ut_k),np.vstack(query_vector))
        
        
    