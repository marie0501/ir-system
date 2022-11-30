from abc import ABC, abstractmethod
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import re
from .document import Document

class Collection(ABC):

    def __init__(self, directory):
        self.directory = directory   
    
    @abstractmethod
    def parse(self):
        pass

    def __remove_stopwords(self,document):
        filtered_list = []
        stop_words = set(stopwords.words("english"))
        for word in document:
            if word.casefold() not in stop_words:
                filtered_list.append(word)

        return filtered_list

    @abstractmethod
    def retrieve_documents(self):
        pass

class Newsgroups(Collection):

    def parse(self):
        documents=[]
        indexed_terms = {}
        count = 0
        current_doc = None

        for file in os.scandir(self.directory):
            for subfile in os.scandir(file):                                  
                current_doc = Document(count,f"File: {file} Subfile: {subfile}")
                with open(subfile) as sf:
                    while True:
                        line = sf.readline()                                                       
                        if not line:
                            documents.append(current_doc)
                            count = count + 1
                            print(count)
                            break
                        line = self.remove_stopwords(word_tokenize(re.sub(r'[^\w\s]', ' ', line)))
                        for term in line:                                  
                            vector = indexed_terms.get(term)
                            if vector == None:
                                vector = [0 for i in range(18828)]
                            vector[count-1]=vector[count-1] + 1
                            indexed_terms.update({term:vector})
        
        return documents, indexed_terms

class Cranfield(Collection):

    def parse(self):
        indexed_terms={}
        documents=[]
        count = 0
        current_doc = None
        max_freq = [0 for i in range(1400)]
                
        with open(self.directory,'r') as f:            
            while True:
                line = f.readline()
                if not line:                    
                    documents.append(current_doc)
                    break
                if line.startswith(".I"):
                    if current_doc != None:
                        documents.append(current_doc)                    
                    current_doc = Document(count + 1, "")
                    count = count + 1
                current_doc.body = current_doc.body + line
                line = self.remove_stopwords(word_tokenize(re.sub(r'[^\w\s]', ' ', line)))
                for term in line:                                  
                    vector = indexed_terms.get(term)
                    if vector == None:
                        vector = [0 for i in range(1401)]
                    elif vector[count-1]==0:
                        vector[1400]=vector[1400]+1
                    vector[count-1]=vector[count-1] + 1
                    if vector[count-1] > max_freq[count-1]:
                        max_freq[count-1] = vector[count-1]
                    indexed_terms.update({term:vector})

        return indexed_terms, documents, max_freq