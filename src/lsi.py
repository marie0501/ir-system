import re, math
import numpy as np
import pickle
import random

class LSI: #IRM
    
    # Crear una matriz term-documento con 3 pesos diferentes:
    #1- Los pesos binarios
    #2- Frecuencia de los pesos
    #3- Con los valores de tf_idf
    def __init__(self, collection, terms, query, binary = False, tfidf=False):
        #super().__init__(collection, terms, query) #la lista de term estan todos los terminos unicos 
        self.collection = collection
        self.terms = terms
        self.query = query
        # de todos los documentos ordenados alfabeticamente
        self.tf_ij = [] #matriz tf
        self.idf_i = [] #matriz idf
        self.tf_idf = [] #matriz tf x idf = w_ij

        self.query_vector = self.get_query_vector()
        self.matrix_term_doc = self.create_matrix_term_document( binary, tfidf)


   #matriz term-document que representa la frecuencia de los terminos en los documentos
    def create_matrix_term_document(self, binary = False, tfidf=False):
        term_vector = []
        m_term_doc = []

        if binary:
            for term in self.terms:
                for doc in self.collection:
                    if term in doc:#doc.body
                        term_vector.append(1)
                    else:
                        term_vector.append(0)

            m_term_doc.append(term_vector.copy())
            term_vector.clear()

        elif tfidf:
            self.__calculate_tf()
            self.__calculate_idf(len(self.collection)) # mandar el total de documentos
            self.__calculate_tf_idf()
            m_term_doc = self.tf_idf.copy()

        #usar la matriz term-doc de frequencia por defecto
        else:
            for term in self.terms:
                for index, doc in enumerate(self.collection):
                    #term_vector.append(len(re.findall(term,doc.body.lower())))
                    term_vector.append( len(re.findall(term,doc.lower())))

                m_term_doc.append(term_vector.copy())
                term_vector.clear()
        
        self.save_matrix(m_term_doc, binary, tfidf)
        return m_term_doc

    #serializacion de las matrices
    def save_matrix(self, M, binary = False, tfidf=False):
        if binary:
            with open("binary_matrix","wb") as binary_file: # wb = escritura binaria
                pickle.dump(M, binary_file)
        elif tfidf:
            with open("tfidf_matrix","wb") as tfidf_file:
                pickle.dump(M, tfidf_file)
        else:
            with open("frequency_matrix","wb") as freq_file: 
                pickle.dump(M, freq_file)

    # deserializacion de las matrices
    def get_matrix(self, binary = False, tfidf=False):
        result = []
        if binary:
            with open("binary_matrix","rb") as binary_file: # rb = lectura binaria
                result = pickle.load(binary_file)
        elif tfidf:
            with open("tfidf_matrix","rb") as tfidf_file: 
                result = pickle.load(tfidf_file)
        else:
            with open("frequency_matrix","rb") as freq_file: 
                result = pickle.load(freq_file)
        return result

    #el doble guion bajo al principio indica q son metodos privados
    def __calculate_tf(self):
        tf_vector = []
        max_freq = self.__select_max() 
        for term_vector in matrix_term_doc:
            for i, freq_d in enumerate(term_vector):
                value = freq_d / float(max_freq[i])
                tf_vector.append(value)
            self.tf_ij.append( tf_vector.copy())
            tf_vector.clear()
       
    #calcula el termino de mayor frecuencia por documento
    def __select_max(self):
        result = [] #len(result) = cantidad de documentos
        for doc_vector in self.matrix_term_doc:
            if len(result) == 0: result = doc_vector
            else:
                for i in range(len(doc_vector)):
                    if result[i] < doc_vector[i]:
                        result[i] = doc_vector[i]
        return result

    # N:la cantidad total de documentos en la coleccion
    # devuelve un dict de term: value= [idf_i, n]
    # donde n es la cantidad de veces q aparece el term i en el total de documentos
    def __calculate_idf(self, N):
        idf_vector=[]
        n_i = 0
        
        for term, term_vector in indexed_terms.items():
            for d in term_vector:
                if d > 0:
                    n_i += 1
            idf = math.log( N / float( n_i))
            idf_vector.append(idf)
            idf_vector.append(n_i)
            self.idf_i.append( idf_vector.copy())
            idf_vector.clear()
        

    def __calculate_tf_idf(self):
        tfidf_vector = []
        
        for term, term_vector in tf_ij.items():
            idf_value = self.idf_i.get(item)[0] #tomar el idf correspondiente al termino i
            for d in term_vector:
                n = idf_value * d
                tfidf_vector.append(n)
            self.tf_idf.append(tfidf_vector.copy())
            tfidf_vector.clear()
    
    #crear el vector consulta con las frecuencias q tiene en cada documento
    def get_query_vector(self):
        query_vector = []
        for term in self.terms:
            freq = len(re.findall(term, self.query.lower()))
            query_vector.append(freq)
        return query_vector
        
    #A es la matriz a la q se le va a aplicar el SVD
    def get_svd(self):
        U, S, VT = np.linalg.svd(self.matrix_term_doc)
        U = np.round(U,4) #redondea hasta 4 valores despues de la coma
        S = np.round(S,4)
        S = np.diag(S)
        VT = np.round(VT,4)

        k = self.__dimension_reduction()
        #reducir la dimension de las matrices 
        rows = len(self.matrix_term_doc)
        columns = len(self.matrix_term_doc[0])
        U2 = U[ : rows, : k]
        S2 = S[0 : k]
        VT2 = VT[ : k, : columns]

        return U2, S2, VT2

    #devuelve el valor k<r, q representa la nueva dimension de las matrices
    #k:cantidad de conceptos < r total de documentos
    def __dimension_reduction(self):
        k = [ 100, 200, 300]
        r = random.randint(0, 2)
        return k[r] # k = entre 100 y 300

    #reducir la dimesion del vector consuta 
    def __query_dimension_reduction(self, U, S):
        query_vector_2 = np.dot(np.dot(np.linalg.inv(S),U.transpose()),self.query_vector)
        query_vector_2 = np.round(query_vector_2,4)
        return query_vector_2

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


collections = ["leon leon leon", "leon leon leon zorro", "leon zorro nutria","leon leon leon zorro zorro zorro", "nutria"]
query = "nutria"
terms = ["leon","zorro","nutria"]
lsi = LSI(collections,terms,query)
ranking = lsi.calculate_ranking()
print(ranking)