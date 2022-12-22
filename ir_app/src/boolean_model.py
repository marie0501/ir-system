from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import time
from sympy.logic import to_dnf
from .irm import IRM
import numpy as np


class Boolean(IRM):
    
    def __init__(self):
        self.name = "boolean"
    
    def search(self, query, collection):
        
        indexed_terms = self._load(collection.name + '\\' + collection.name + '_indexed_terms')         
        tokenized_logical_query = self.__tokenize_logical_query(query)
        query_vector = self.__process_query(tokenized_logical_query, indexed_terms, collection.number_of_documents())   
        if len(query_vector) < 1:
            tokenized_query = self.__tokenize_query(query)
            query_vector = self.__process_query(tokenized_query,indexed_terms,collection.number_of_documents())              
        retrieved_documents_similarity = self.__get_relevant_documents(query_vector)       
        
        self._save(retrieved_documents_similarity,self.name + '_retrieved_documents_similarity') 

        return collection.retrieve_documents(retrieved_documents_similarity, self.name)      

    def __tokenize_query(self, query):

        tokenized_query = self._remove_stopwords(word_tokenize(re.sub(r'[^\w\s]', ' ', query)))

        for i in range(1,(2*len(tokenized_query))-1,2):
            tokenized_query.insert(i,'or')

        return tokenized_query   



    def __tokenize_logical_query(self, query):
        
        stop_words = set(stopwords.words("english"))
        tokenized_query = word_tokenize(re.sub('[^\w ()\[\]]+',' ',query))
        symbols_set =set({'and','or','not','(',')'})
        n=len(tokenized_query)
        i =0
        inserted_ands = 0

        while i - inserted_ands < n-1:

            if tokenized_query[i] not in symbols_set and tokenized_query[i+1] not in symbols_set:
                tokenized_query.insert(i+1,'or')
                inserted_ands+=1
            i+=1                

        return tokenized_query
     
    def __precedence(self,op):

        if op == 'or':
            return 1
        elif op == 'and':
            return 2
        elif op == 'not':
            return 3

        return 0

    def __op_or(self,x,y):
        vector_result=[]
        for i in range(len(x)):
                    if x[i] == 0 and y[i] == 0:
                        vector_result.append(0)
                    else:
                        vector_result.append(1)

        return vector_result

    def __op_and(self,x,y):
        vector_result=[]
        for i in range(len(x)):
                    if x[i] > 0 and y[i] > 0:
                        vector_result.append(1)
                    else:
                        vector_result.append(0)
        return vector_result

    def __op_not(self,x):
        vector_result=[]        
        for i in range(len(x)):
                    if x[i] > 0:
                        vector_result.append(0)
                    else:
                        vector_result.append(1)
        return vector_result

    
    # Function that returns value of
    # expression after evaluation.
    def __process_query(self,tokens, indexed_terms, number_of_documents):

        # stack to store integer values.
        values = []

        operators = {
        'and' : lambda x,y : self.__op_and(x,y),
        'or' : lambda x,y : self.__op_or(x,y),
        'not' : lambda x : self.__op_not(x)
    }

        # stack to store operators.
        ops = []
        i = 0

        try: 
                    
            while i < len(tokens):       

                # Current token is an opening
                # brace, push it to 'ops'
                if tokens[i] == '(':
                    ops.append(tokens[i])

                elif tokens[i] not in set(operators.keys()) and tokens[i]!=')':

                    term_vector = None
                    try:
                        term_vector = np.delete(indexed_terms[tokens[i]],number_of_documents)
                    except:
                        term_vector=[0 for i in range(number_of_documents)]
                    
                    values.append(term_vector)

                # Closing brace encountered,
                # solve entire brace.
                elif tokens[i] == ')':
                
                    while len(ops) >0 and ops[-1] != '(':
                    
                        op = ops.pop()

                        if op == 'not':
                            val1 = values.pop()
                            values.append(operators[op](val1))
                        else:
                            val2 = values.pop()
                            val1 = values.pop()
                            values.append(operators[op](val1, val2))

                    # pop opening brace.
                    ops.pop() 

                    if len(ops)>0 and ops[-1]=='not':
                        op =ops.pop()
                        val1 = values.pop()
                        values.append(operators[op](val1))                      

                # Current token is an operator.
                elif tokens[i] in set(operators.keys()):

                    while (len(ops) != 0 and self.__precedence(ops[-1]) >= self.__precedence(tokens[i])):

                        op = ops.pop()

                        if op == 'not':
                            val1 = values.pop()
                            values.append(operators[op](val1))
                        else:
                            val2 = values.pop()
                            val1 = values.pop()
                            values.append(operators[op](val1, val2))

                    # Push current token to 'ops'.
                    ops.append(tokens[i])

                i += 1

            # Entire expression has been parsed
            # at this point, apply remaining ops
            # to remaining values.
            while len(ops) != 0:

                op = ops.pop()

                if op == 'not':
                    val1 = values.pop()
                    values.append(operators[op](val1))
                else:
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(operators[op](val1, val2))

            # Top of 'values' contains result,
            # return it.
            return values[-1]

        except Exception as ex:
            print(ex)
            return []

    def __get_relevant_documents(self, query_vector):
    
        retrieved_documents = {}
        for i in range(len(query_vector)):
            if query_vector[i] > 0:
                retrieved_documents.update({i:1})

        return retrieved_documents

    




 
   
 

  

       



    


  
        
        