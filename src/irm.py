from abc import ABC, abstractmethod
import pickle

class IRM:
    def __init__(self):
        pass

    @abstractmethod
    def search(self):
        pass

    def _load(self,name):
        with open(name,'rb') as f:
            return pickle.load(f)