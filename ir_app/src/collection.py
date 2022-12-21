from abc import ABC, abstractmethod
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import re
import pickle
import time
from .document import Document
import json


class Collection(ABC):

    def __init__(self, directory):
        self.directory = directory 
          
    
    @abstractmethod
    def parse_documents(self, filename):
        pass
    
    @abstractmethod
    def retrieve_documents(self, documents):
        pass

    @abstractmethod
    def number_of_documents():
        pass

    @abstractmethod
    def parse_querys(self, file_name):
        pass

    @abstractmethod
    def parse_relevant_documents(self, file_name):
        pass

    def _remove_stopwords(self, document):
        filtered_list = []
        stop_words = set(stopwords.words("english"))
        for word in document:
            if word.casefold() not in stop_words:
                filtered_list.append(word.casefold())

        return filtered_list

    def save(self, file, name):
         with open("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Proyecto Final\\Proyecto\\ir_system\\ir_app\\data\\" + name,'wb') as f:
            pickle.dump(file, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self,name):
        with open("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Proyecto Final\\Proyecto\\ir_system\\ir_app\\data\\" + name,'rb') as f:
            return pickle.load(f)



class Cranfield(Collection):

    def __init__(self, directory):
        self.name='cranfield'
        super().__init__(directory)

    def parse_documents(self, file_name):

        indexed_terms={}
        documents={}
        current_doc = None
        max_freq = [0 for i in range(1400)] 
        path = self.directory + '\\' + file_name       
                
        with open(path ,'r') as f:            
            while True:
                line = f.readline()
                if not line:                    
                    documents.update({current_doc.id:current_doc})
                    break
                elif line.startswith(".I"):
                    if current_doc != None:
                        documents.update({current_doc.id:current_doc})                    
                    current_doc = Document(int(line.split()[1]), "", "", "","")
                    line = f.readline()
                    if line.startswith('.T'):
                        line = f.readline()
                        while not line.startswith('.A'):                            
                            current_doc.title += line
                            line = f.readline()
                        line = f.readline()
                        while not line.startswith('.B'):
                            current_doc.author += line
                            line = f.readline()
                        line = f.readline()
                        while not line.startswith('.W'):
                            current_doc.place += line 
                            line = f.readline()
                        continue          
                                
                current_doc.body = current_doc.body + line
                line = self._remove_stopwords(word_tokenize(re.sub(r'[^\w\s]', ' ', line)))
                for term in line:                                  
                    vector = indexed_terms.get(term)
                    if vector == None:
                        vector = [0 for i in range(1401)]
                    elif vector[current_doc.id-1]==0:
                        # last position has the total of documents the term appears
                        vector[1400]=vector[1400]+1
                    vector[current_doc.id-1]=vector[current_doc.id-1] + 1
                    if vector[current_doc.id-1] > max_freq[current_doc.id-1]:
                        max_freq[current_doc.id-1] = vector[current_doc.id-1]
                    indexed_terms.update({term:vector})

        self.save(indexed_terms,'cranfield\\cranfield_indexed_terms')
        self.save(documents,'cranfield\\cranfield_documents')
        self.save(max_freq,'cranfield\\cranfield_max_freq')

             
        
    def parse_querys(self, file_name):

        querys = {}
        path = self.directory + '\\' + file_name 
        index = r'.I [0-9][0-9][0-9]'
               
        current_index = 0
        current_query =''

        with open(path ,'r') as f:            
            while True:
                line = f.readline()
                if not line:                    
                    querys.update({current_index:current_query})
                    break
                
                else:
                    match=re.match(index, line)
                    if match != None:
                        if len(current_query) > 0:
                            querys.update({current_index:current_query})
                            current_query = ''   
                        current_index = int(match.group().split()[1])                         
                    elif line.startswith('.W'):
                        continue
                    else:                               
                        current_query+=line  


        self.save(querys,'cranfield\\cranfield_querys')
                          
                    
    def parse_relevant_documents(self, file_name):
        
        relevant_documents ={}     #dic {query id: [list of relevant documents id]}
        path = self.directory + '\\' + file_name 
        

        with open(path ,'r') as f:            
            while True:
                line = f.readline().split()
                if not line:                    
                    break
                
                else:                    
                    query_index = int(line[0])
                    relevant_document_id = int(line[1])
                    if not query_index in relevant_documents.keys():
                        relevant_documents.update({query_index:set()})
                    relevant_documents.get(query_index).add(relevant_document_id)

                

        self.save(relevant_documents,'cranfield\\cranfield_relevant_documents')


    def retrieve_documents(self, relevant_documents):
        
        documents = self.load('cranfield\\cranfield_documents')
        retrieved_documents = []
        for key in relevant_documents.keys():
            documents[key+1].score = relevant_documents[key]
            retrieved_documents.append(documents[key+1])                

        return  retrieved_documents

    def number_of_documents(self):
        return 1400

class Scifact(Collection):
    def __init__(self, directory):
        self.name = 'scifact'
        super().__init__(directory)


    def parse_documents(self, file_name):

        indexed_terms = {}
        documents = {}
        current_doc = None
        max_freq = [0 for i in range(2000)] 
        path = self.directory + '\\' + file_name 
        doc_format = r'{"_id": ".*", "title": ".*", "text": ".*", "metadata": {}}'
              

        with open(path,'r') as f:
            data = f.read()

        data_docs = re.findall(doc_format, data)
        count=0
        

        if data_docs != None:
            
            for i in range(2000):
                document = re.findall(r'".*?": ".*?"', data_docs[i])

                id = document[0].split(':')[1].removeprefix('"').removesuffix('"')
                title = document[1].split(':')[1].removeprefix('"').removesuffix('"')
                text = document[2].split(':')[1].removeprefix('"').removesuffix('"')

                documents.update({id:Document(id,title,"","",text)})
                current_text = self._remove_stopwords(word_tokenize(re.sub(r'[^\w\s]', ' ', text)))
                for term in current_text:                                  
                    vector = indexed_terms.get(term)
                    if vector == None:
                        vector = [0 for i in range(2001)]
                    elif vector[count]==0:
                        # last position has the total of documents the term appears
                        vector[2000]=vector[2000]+1
                    vector[count]=vector[count] + 1
                    if vector[count] > max_freq[count]:
                        max_freq[count] = vector[count]
                    indexed_terms.update({term:vector})

                count+=1                

        self.save(indexed_terms,'scifact\\scifact_indexed_terms')
        self.save(documents,'scifact\\scifact_documents')
        self.save(max_freq,'scifact\\scifact_max_freq')

        print(len(indexed_terms.keys()))
        
    def parse_querys(self, file_name):

        querys = {}  
        path = self.directory + '\\' + file_name        
        querys_format = r'{"_id": ".*", "text": ".*", .*}'
        
        with open(path,'r') as f:
            data = f.read()

        data_querys = re.findall(querys_format,data)
 
        for i in range(200):

            current_query = re.findall(r'".*?": ".*?"', data_querys[i])
            
            id = int(current_query[0].split(':')[1].replace('"',''))
            text = current_query[1].split(':')[1]
            
            querys.update({id:text})

        self.save(querys, 'scifact\\scifact_querys')

      
    def parse_relevant_documents(self, file_name):
        
        querys = self.load('scifact\\scifact_querys')
        document_parsed = self.load('scifact\\scifact_documents')
        path = self.directory + '\\' + file_name
        
        relevant_documents = {}

        with open(path ,'r') as f: 
            f.readline()           
            while True:
                line = f.readline().split()
                if not line:                    
                    break
                
                else:                    
                    query_index = int(line[0])
                    relevant_document_id = int(line[1])                    
                    if not query_index in set(relevant_documents.keys()):
                        relevant_documents.update({query_index:set()})
                    relevant_documents.get(query_index).add(relevant_document_id)

                        
                  

        self.save(relevant_documents, 'scifact\\scifact_relevant_documents')




    def retrieve_documents(self, documents):
        return super().retrieve_documents(documents)

    def number_of_documents(self):
        return 2000 
    
   
