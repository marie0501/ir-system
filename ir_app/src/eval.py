
class Eval:

    def precision(self, retrieved, relevant):
        if retrieved == 0:
            return 0
        return relevant/retrieved

    def recall(self, relevant, retrieved):
        if relevant == 0:
            return 0
        return retrieved/relevant
        
        