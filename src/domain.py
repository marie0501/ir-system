from abc import ABC, abstractmethod
from multiprocessing.resource_sharer import stop
import os
from matplotlib.lines import VertexSelector
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import numpy as np

DIR = "C:\\Users\\Marie\\Desktop\\New folder\\New folder"

class Document:
    
    def __init__(self,id, title, author, body):
        self.id = id
        self.title = title
        self.author= author
        self.body = body

    def __repr__(self):
        return f"Title: {self.title}\n"


class Collection(ABC):

    def __init__(self, directory):
        self.directory = directory   
    
    @abstractmethod
    def parse(self):
        pass

    def remove_stopwords(self,document):
        filtered_list = []
        stop_words = set(stopwords.words("english"))
        for word in document:
            if word.casefold() not in stop_words:
                filtered_list.append(word)

        return filtered_list

    

class BooleanIRM:

    boolean_op =['and', 'or', 'not']

    def __init__(self, collection, terms, query):
        self.collection = collection
        self.terms = terms
        self.query = query
        self.indexed_terms = {}
        self.indexing_terms()
   

    def indexing_terms(self):
        temp = []

        for term in self.terms:
            for doc in self.collection:
                if term in doc.body:
                    temp.append(1)
                else:
                    temp.append(0)

            self.indexed_terms.update({term : temp.copy()})
            temp.clear()
        

    def filter_query(self):

        list = []
     
        for term in self.query:
            if term == 'but' or term in self.boolean_op or term in self.terms:
                list.append(term)

        if not any(item in list for item in ['and','or','not','but']):
                     
            for i in range(1,(len(list)*2)-1,2):
                list.insert(i,'and')
               
        self.query = list
     

    def process_query(self):

        bit_wise_op=''
        self.filter_query()
        previous_term_incidence = []
        next_term_incidence = []
        result_set = []
        has_previous_term=False
        has_not_op=False        

        for term in self.query:
            if (not term in self.boolean_op) and term != 'but':

                if has_not_op:
                    if has_previous_term:
                        next_term_incidence = self.process_boolean_op('not', self.indexed_terms[term], next_term_incidence)
                    else:
                        previous_term_incidence = self.process_boolean_op('not', self.indexed_terms[term], next_term_incidence)
                        result_set = previous_term_incidence

                    has_not_op=False

                elif not(has_previous_term):
                    previous_term_incidence=self.indexed_terms[term]
                    result_set=previous_term_incidence
                    has_previous_term = True

                else:
                    next_term_incidence = self.indexed_terms[term]

            elif term == 'not':
                has_not_op = True

            else:
                if term == 'but':
                    bit_wise_op = 'and'
                else:
                    bit_wise_op = term
            
            if len(next_term_incidence) != 0 and not(has_not_op):
                result_set = self.process_boolean_op(bit_wise_op, previous_term_incidence, next_term_incidence)
                previous_term_incidence = result_set
                has_previous_term = True
                next_term_incidence = []

        return result_set

    def process_boolean_op(self, op, previous_term, next_term):

        result_set=[]

        if op == 'not':
            for i in previous_term:
                if i == 1:
                    result_set.append(0)
                else:
                    result_set.append(1)

        elif op == 'and':
            for i in range(len(previous_term)):
                if previous_term[i] == 1 and next_term[i]==1:
                    result_set.append(1)
                else:
                    result_set.append(0)

        elif op == 'or':
            for i in range(len(previous_term)):
                if previous_term[i] == 0 and next_term[i]==0:
                    result_set.append(0)
                else:
                    result_set.append(1)

        return result_set

    def retrieve_documents(self):

        vector = self.process_query()
        relevant_documents = []

        for i in range(len(vector)):
            if vector[i] == 1:
                relevant_documents.append(self.collection[i])

        return relevant_documents


class Newsgroups(Collection):

    def __init__(self, directory):
        super().__init__(directory)       

    def parse(self):
        documents=[]
        terms = set([])
        count = 0
        
        for file in os.scandir(self.directory):
            for subfile in os.scandir(file):
                with open(subfile) as sf:
                    author = sf.readline()
                    title = sf.readline()
                    text = self.remove_stopwords(word_tokenize(re.sub(r'[^\w\s]', ' ', sf.read().lower())))

                    documents.append(Document(count,title[9:], author[6:], text))
                    terms = terms | set(text)
                    count+=1

        return documents, list(terms)

    def remove_stopwords(self,document):
        return super().remove_stopwords(document)
 

def start(collection, irm, query):

    collections = {'newsgroup': lambda d : Newsgroups(d)}
    irms = {'boolean': lambda c,t,q : BooleanIRM(c,t,q)}

    query = (re.sub(r'[^\w\s]', ' ', query.lower())).split(' ')

    col, terms = collections[collection](DIR).parse()

    model = irms[irm](col,terms,query)

    return model.retrieve_documents()

  

       

print("Write a query: ")
query=input()
start('newsgroup','boolean', query)






    
        

    

    


  
        
        