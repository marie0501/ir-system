import glob
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import stopwords
import string
from collections import Counter
import numpy as np
from collections import OrderedDict
from .irm import IRM
import re


class Vectorial(IRM):

    def search(self, query, collection, indexed_terms, max_freq):

        term_document_matrix = self.__create_term_document_matrix(indexed_terms, max_freq)
        query_vector = self.__process_query(query, term_document_matrix)
        relevant_documents = self.__similarity(term_document_matrix, query_vector)

        return collection.retrieve_documents(relevant_documents)

    def __create_term_document_matrix(self, indexed_terms, max_freq):

        tf_matrix = self.__create_tf_matrix(indexed_terms, max_freq)
        idf_matrix = self.__create_idf_matrix(indexed_terms, len(max_freq))
        tf_idf_matrix = self.__create_tf_idf_matrix(tf_matrix, idf_matrix)

        return tf_idf_matrix
        
    def __create_tf_matrix(self, indexed_terms, max_freq):

        tf_matrix = []
        for key in indexed_terms.keys:
            current_vector = indexed_terms[key]
            for i in range(len(max_freq)):
                current_vector[i]= current_vector[i] / max_freq[i]
            tf_matrix.append(current_vector)

        return tf_matrix                


    def __create_idf_matrix(self, indexed_terms, N):

        idf_matrix = []
        for key in indexed_terms.keys:
            if indexed_terms[key][N]!=0:
                idf_matrix.append(np.log10(N/indexed_terms[key][N]))

        return idf_matrix

    def __create_tf_idf_matrix(self, tf_matrix, idf_matrix):

        tf_idf_matrix = []
        for i in range(len(idf_matrix)):
            for j in range(len(tf_matrix)):
                tf_idf_matrix = tf_matrix[i][j]*idf_matrix[i]

        return tf_idf_matrix

    def __process_query(self, query, indexed_terms, idf_matrix, a):

        query_tokenized = self.remove_stopwords(word_tokenize(re.sub(r'[^\w\s]', ' ', query)))
        query_terms = {}
        max_freq = 0
        query_vector = []
        i=0

        for term in query:
            current_value = 0
            if term in query_terms.keys():
                current_value = query_terms[term]
            query_terms.update({term:current_value})
            if current_value > max_freq:
                max_freq = current_value

        for term in indexed_terms.keys():
            if term in query_terms.keys():
                query_vector.append((a + (a*query_terms[term])/max_freq)*idf_matrix[i])
            else:
                query_vector.append(a * idf_matrix[i])
            i+=1

        return query_vector


    def __similarity(self, term_document_matrix, query_vector):

        sim = {}
        sim_current_doc = 0

        for i in range(term_document_matrix.shape[1]):
            for j in range(term_document_matrix.shape[0]):
                sim_current_doc += (term_document_matrix[j][i]*query_vector[j])/(np.sq(term_document_matrix[j][i]**2)*(np.sq(query_vector[j]**2)))
            if sim_current_doc > 0.3:
                sim.update({i:sim_current_doc})

        return sorted(sim.items(), key=lambda x: x[1], reverse=True)

    

            

                

        




            


        




        




