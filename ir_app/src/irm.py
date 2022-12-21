from abc import ABC, abstractmethod
import pickle
from os.path import exists
from nltk.corpus import stopwords
from nltk import word_tokenize

class IRM:
    def __init__(self):
        pass

    @abstractmethod
    def search(self):
        pass

    def _load(self,name):
        if exists("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Proyecto Final\\Proyecto\\ir_system\\ir_app\\data\\" + name):
            with open("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Proyecto Final\\Proyecto\\ir_system\\ir_app\\data\\" + name,'rb') as f:
                return pickle.load(f)
        return []

    def _save(self, file, name):
         with open("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Proyecto Final\\Proyecto\\ir_system\\ir_app\\data\\" + name,'wb') as f:
            pickle.dump(file, f, protocol=pickle.HIGHEST_PROTOCOL)

    def _remove_stopwords(self, query):
        filtered_list = []
        stop_words = set(stopwords.words("english"))
        for word in query:
            if word.casefold() not in stop_words:
                filtered_list.append(word.casefold())

        return filtered_list