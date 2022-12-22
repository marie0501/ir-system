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
            relevant_documents_model = set(self.collection.load(f'{self.collection.name}\\{self.collection.name}_{self.model.name}_relevant_documents_ids'))
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
        m = 'recobrado'
        if method == 'precision':
            m='precisión'
    
        x = list(result.keys())
        y = []

        for i in x:
            y.append(result[i])
            
        plt.scatter(x,y, label='modelo ' + self.model.name, c='g')
        
        plt.title(m.capitalize(), loc = 'left')
        plt.xlabel('consultas')
        plt.ylabel(m)
        
        plt.legend()
        plt.show()


            



