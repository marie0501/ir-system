from nltk.corpus import stopwords
from nltk import word_tokenize
import numpy as np
from .irm import IRM
import re
import math



class Vectorial(IRM):

    def search(self, query, collection, indexed_terms_name, max_freq_name):

        indexed_terms = self._load(indexed_terms_name)
        max_freq = self._load(max_freq_name)
        tf_matrix = self.__create_tf_matrix(indexed_terms, max_freq)
        idf_matrix = self.__create_idf_matrix(indexed_terms, len(max_freq))
        term_document_matrix = self.__create_tf_idf_matrix(tf_matrix, idf_matrix)
        query_vector = self.__process_query(query, indexed_terms, idf_matrix, 0.5)
        relevant_documents = self.__similarity(term_document_matrix, query_vector)

        return collection.retrieve_documents(relevant_documents)

            
    def __create_tf_matrix(self, indexed_terms, max_freq):

        tf_matrix =[]
        for key in indexed_terms.keys():
            current_vector = np.delete(indexed_terms[key], len(max_freq))
            for i in range(len(max_freq)):
                print(current_vector[i])
                print(max_freq[i])
                current_vector[i]= current_vector[i]/max_freq[i]
                print(current_vector[i])
            tf_matrix.append(current_vector)

        return np.array(tf_matrix)             


    def __create_idf_matrix(self, indexed_terms, N):

        idf_matrix = []
        for key in indexed_terms.keys():
            if indexed_terms[key][N]!=0:
                idf_matrix.append(np.log10(N/indexed_terms[key][N]))
            else:
                idf_matrix.append(0)

        return np.array(idf_matrix)

    def __create_tf_idf_matrix(self, tf_matrix, idf_matrix):

        tf_idf_matrix = []
        for i in range(tf_matrix.shape[0]):
            current_array = []
            for j in range(tf_matrix.shape[1]):
                current_array.append(tf_matrix[i][j]*idf_matrix[i])
            tf_idf_matrix.append(current_array)

        return np.array(tf_idf_matrix)

    def __process_query(self, query, indexed_terms, idf_matrix, a):

        tokenized_query = word_tokenize(re.sub(r'[^\w\s]', ' ', query))
        stop_words = set(stopwords.words("english"))
        query_terms = {}
        max_freq = 0
        query_vector = []
        i=0

        for term in tokenized_query:
            current_value = 1
            if term in stop_words:
                continue
            if term in query_terms.keys() and term not in stopwords:
                current_value = query_terms[term] + 1
            query_terms.update({term:current_value})
            if current_value > max_freq:
                max_freq = current_value
        print(max_freq)
        for term in indexed_terms.keys():
            if term in query_terms.keys():
                query_vector.append((a + ((a*query_terms[term])/max_freq))*idf_matrix[i])
            else:
                query_vector.append(a * idf_matrix[i])
            i+=1

        return np.array(query_vector)


    def __similarity(self, term_document_matrix, query_vector):

        sim = {}
        print(query_vector.shape)
        
        print(term_document_matrix.shape)
        for i in range(term_document_matrix.shape[0]):
            sim_current_doc = 0
            for j in range(term_document_matrix.shape[1]):
                sim_current_doc += (term_document_matrix[i][j]*query_vector[i])/(math.sqrt(term_document_matrix[i][j]**2)*(math.sqrt(query_vector[i]**2)))
                print(sim_current_doc)
            if sim_current_doc > 0.3:
                sim.update({i:sim_current_doc})        

        return sim

    

            

                

        




            


        




        




