import numpy as np
import random
from .vectorial_model import Vectorial
from scipy.sparse.linalg import svds


class LSI(Vectorial):    
    
    def search(self, query, collection, indexed_terms_name, max_freq_name):
        
        k=200
        indexed_terms = self._load(indexed_terms_name)
        max_freq = self._load(max_freq_name)
        tf_matrix = self._create_tf_matrix(indexed_terms, max_freq)
        idf_matrix = self._create_idf_matrix(indexed_terms, len(max_freq))
        term_document_matrix = self._create_tf_idf_matrix(tf_matrix, idf_matrix)
        U,S,Vt = svds(term_document_matrix,k)
        query_vector = self._process_query(query, indexed_terms, idf_matrix, 0.5)
        query_k = self.__query_low_rank_approx(query_vector,U,S)
        relevant_documents = self._similarity(term_document_matrix, query_vector)

        return collection.retrieve_documents(relevant_documents)

                
        
    #reducir la dimesion del vector consuta 
    def __query_low_rank_approx(self,query_vector, U, S):

        return np.dot(np.dot(np.linalg.inv(S),U.transpose()),query_vector)
        
        
    #Calcular la similitud de term-doc
    # para cuantificar la similitud entre un vector consulta y un vector documento
    # solo necesitamos verificar los vectores propios en la matriz VT.
    # Esta métrica se conoce como: similitud de coseno
    def similarity(self, doc_j, query):
        #result = np.dot(doc_j, query)
        result = 0
        doc_j_norm = np.linalg.norm(doc_j) ##frobenius norm
        query_norm = np.linalg.norm(query) ##frobenius norm
        for i in range(0,min(len(doc_j),len(query))):
            result +=  doc_j[i, 0] * query[i]
        result /= doc_j_norm * query_norm
        return result

    #Devuelve el ranking de los documentos relevantes a la consulta de mayor a menor relevancia
    def calculate_ranking(self):
        U, S, VT = self.get_svd()
        query_vector = self.__query_dimension_reduction(U,S)
        sim = 0
        rank = {}
        for i in range(len(VT[0])):# len(VT[0]) => indica la cantidad de columnas
            doc_column = VT[:,i:i + 1]
            sim = np.round(self.similarity(doc_column, query_vector),4)
            doc_name = collections[i] #collections[i].id
            rank.update({doc_name : sim})
        
        result = dict(sorted(rank.items(), key = lambda item: item[1], reverse=True))
        return result


#collections = ["leon leon leon", "leon leon leon zorro", "leon zorro nutria","leon leon leon zorro zorro zorro", "nutria"]
#query = "nutria"
#terms = ["leon","zorro","nutria"]
#lsi = LSI(collections,terms,query,False,True)
#ranking = lsi.calculate_ranking()
#print(ranking)