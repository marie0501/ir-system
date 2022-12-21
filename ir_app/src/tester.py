from .eval import Eval
import matplotlib.pyplot as plt
import numpy as np

class Tester:

    def __init__(self, collection, model):
        self.collection=collection
        self.model=model
    
    def test(self, method = 'precision'):

        result = {}

        querys = self.collection.load(self.collection.name + '\\' + self.collection.name + '_querys')
        relevant_documents = self.collection.load(self.collection.name + '\\' + self.collection.name + '_relevant_documents')
        eval = Eval()
        keys = set(querys.keys()).intersection(set(relevant_documents.keys()))
       
        for key in keys:
            query = querys[key]
            self.model.search(query, self.collection)
            relevant_documents_model = set((self.collection.load(self.model.name + '_retrieved_documents_similarity')).keys())
            relevant_documents_query = set(relevant_documents.get(key))

            if method == 'recall': 
                recall = eval.recall(len(relevant_documents_query), len(relevant_documents_query.intersection(relevant_documents_model)))   
                result.update({key:recall}) 
                print('Query: ' + str(key))         
                
            else:
                precision = eval.precision(len(relevant_documents_model),len(relevant_documents_query.intersection(relevant_documents_model)))
                result.update({key:precision})
                print('Query: ' + str(key))
                print(precision)

        self.collection.save(result, self.collection.name + '\\' + self. collection.name + '_' + self.model.name + '_' + method)

    def plot(self,method='precision'):

        result = self.collection.load(self.collection.name + '\\' + self. collection.name + '_' + self.model.name + '_' + method)

        x = list(result.keys())
        y = []

        for i in x:
            y.append(result[i])
            
        plt.plot(x,y, label = self.model.name + ' model')
        
        plt.title(method.capitalize(), loc = 'left')
        plt.xlabel('querys id')
        plt.ylabel(method)
        
        plt.legend()
        plt.show()


            



