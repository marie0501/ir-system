from nltk import word_tokenize
import numpy as np
from numpy.linalg import norm
from .irm import IRM
import re
import math
from abc import ABC,abstractmethod




class Vectorial(IRM, ABC):

    def __init__(self):
        self.name = "vectorial"
    
    def search(self, query, collection):
        
        term_document_matrix = self._get_matrix(collection)
        indexed_terms = self._load(collection.name + '\\' + collection.name + '_indexed_terms')
        idf_matrix = self._load(collection.name + '\\' + collection.name + '_idf_matrix')
        query_vector = self._process_query(query, indexed_terms, idf_matrix, 0.5)
        retrieved_documents_similarity = self._similarity(term_document_matrix, query_vector)

        self._save(retrieved_documents_similarity,self.name + '_retrieved_documents_similarity')

        return collection.retrieve_documents(retrieved_documents_similarity,self.name)

    def _get_matrix(self, collection):

        matrix= self._load(collection.name + '\\' + collection.name + '_term_document_matrix')
        
        if len(matrix) < 1:
            indexed_terms = self._load(collection.name + '\\' + collection.name + '_indexed_terms')
            max_freq = self._load(collection.name + '\\' + collection.name + '_max_freq')
            tf_matrix = self._create_tf_matrix(indexed_terms, max_freq)
            idf_matrix = self._create_idf_matrix(indexed_terms, len(max_freq))
            matrix = self._create_tf_idf_matrix(tf_matrix, idf_matrix)

            self._save(tf_matrix, collection.name + '\\' + collection.name + '_tf_matrix')
            self._save(idf_matrix, collection.name + '\\' + collection.name + '_idf_matrix')
            self._save(matrix, collection.name + '\\' + collection.name + '_term_document_matrix')

        return matrix

    def _create_tf_matrix(self,indexed_terms, max_freq):
        print('enter tf')
        tf_matrix =[]
        
        for key in indexed_terms.keys():
            current_vector = np.delete(indexed_terms[key], len(max_freq))
            tf_vector = np.empty((len(current_vector)))
            for i in range(len(current_vector)):
                if current_vector[i] > 1e-15:
                    tf_vector[i]=np.round(current_vector[i]/max_freq[i],4)
                else:
                    tf_vector[i]=0

            tf_matrix.append(tf_vector)
        print('finish tf')
        return np.array(tf_matrix)         


    def _create_idf_matrix(self, indexed_terms, N):
        print('enter idf')
        idf_matrix = []        
        for key in indexed_terms.keys():
            if indexed_terms[key][N] > 10e-16:
                idf = np.log10(N/indexed_terms[key][N])
                idf_matrix.append(idf)
            else:
                idf_matrix.append(0)
        print('finish idf')

        return np.array(idf_matrix)

    def _create_tf_idf_matrix(self, tf_matrix, idf_matrix):
        print('enter tf-idf')
        tf_idf_matrix = []
        for i in range(tf_matrix.shape[0]):
            current_array = []
            for j in range(tf_matrix.shape[1]):
                current_array.append(tf_matrix[i][j]*idf_matrix[i])
            tf_idf_matrix.append(current_array)
        print('finish tf-idf')
        return np.array(tf_idf_matrix)

    def _process_query(self, query, indexed_terms, idf_matrix, a):

        tokenized_query = self._remove_stopwords(word_tokenize(re.sub(r'[^\w\s]', ' ', query)))
        query_terms = {}
        max_freq = 0
        query_vector = []
        i=0

        for term in tokenized_query:
            current_value = 1
            if term in query_terms.keys():
                current_value = query_terms[term] + 1
            query_terms.update({term:current_value})
            if current_value > max_freq:
                max_freq = current_value
        
        for term in indexed_terms.keys():
            if term in query_terms.keys():
                query_vector.append((a + (1-a)*(query_terms[term]/max_freq))*idf_matrix[i])        
            else:
                query_vector.append(a * idf_matrix[i])
            i+=1

        return np.array(query_vector)



    def _similarity(self, term_document_matrix, query_vector):

        sim ={}

        for i in range(term_document_matrix.shape[1]):
            doc_vector = term_document_matrix[:,i]
            doc_vector_norm = np.round(norm(doc_vector),4)
            query_vector_norm = np.round(norm(query_vector),4)
            sim_current_doc = 0

            if doc_vector_norm > 1e-4 and query_vector_norm > 1e-4:
                sim_current_doc = np.matmul(doc_vector,query_vector) / (doc_vector_norm*query_vector_norm)
            
            if sim_current_doc > 0.1:
                sim.update({i:sim_current_doc})

        return dict(sorted(sim.items(), key = lambda item: item[1], reverse=True))


                
    

    

            

                

        




            


        




        




