from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import time
from .collection import Newsgroups, Cranfield
from .irm import IRM


DIR = "C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\20 Newsgroups\\20news-18828"

    

class Boolean(IRM):

    boolean_op =['and', 'or', 'not']

    def __init__(self, collection, terms, query):
        self.collection = collection
        self.terms = terms
        self.query = query
        self.indexed_terms = {}
        start = time.time()
        print("start indexing terms")
        self.indexing_terms()
        end = time.time()
        print(f"end indexing terms {end-start}")
   

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

         
        for term in self.query:
            if term in self.boolean_op or term in self.terms:
                list.append(term)

        if not any(item in list for item in ['and','or','not','but']):
                     
            for i in range(1,(len(list)*2)-1,2):
                list.insert(i,'and')
               
        self.query = list

    def __process_query(self, query):

        query_tokenized = word_tokenize(re.sub('[^\w ()\[\]]+',' ',query))
        boolean_op ={
            'and': '&',
            'not':'~',
            'or':'|'
            }

        for i in range(len(query_tokenized)):
            if query_tokenized[i] in boolean_op.keys():
                query_tokenized[i]=boolean_op[query_tokenized[i]]
        
        




    def __process_dnf_query(self):

        bitwise_op = ''
        self.filter_query()
        previous_term_incidence = []
        next_term_incidence = []
        vector_result = []
        has_previous_term = False
        has_not_op = False        

        for term in self.query:
            if not term in self.boolean_op:
                if has_not_op:
                    if has_previous_term:
                        next_term_incidence = self.__process_boolean_op('not', self.indexed_terms[term], next_term_incidence)
                    else:
                        previous_term_incidence = self.__process_boolean_op('not', self.indexed_terms[term], next_term_incidence)
                        vector_result = previous_term_incidence

                    has_not_op=False

                elif not(has_previous_term):
                    previous_term_incidence = self.indexed_terms[term]
                    vector_result = previous_term_incidence
                    has_previous_term = True

                else:
                    next_term_incidence = self.indexed_terms[term]

            elif term == 'not':
                has_not_op = True

            else:              
                bitwise_op = term
            
            if len(next_term_incidence) != 0 and not(has_not_op):
                vector_result = self.__process_boolean_op(bitwise_op, previous_term_incidence, next_term_incidence)
                previous_term_incidence = vector_result
                has_previous_term = True
                next_term_incidence = []

        return vector_result

    def __process_boolean_op(self, op, previous_term, next_term):

        vector_result=[]

        if op == 'not':
            for i in previous_term:
                if i == 1:
                    vector_result.append(0)
                else:
                    vector_result.append(1)

        elif op == 'and':
            for i in range(len(previous_term)):
                if previous_term[i] == 1 and next_term[i]==1:
                    vector_result.append(1)
                else:
                    vector_result.append(0)

        elif op == 'or':
            for i in range(len(previous_term)):
                if previous_term[i] == 0 and next_term[i]==0:
                    vector_result.append(0)
                else:
                    vector_result.append(1)

        return vector_result

    def retrieve_documents(self):
        start = time.time()
        print("start processing query")
        vector = self.process_query()
        end = time.time()
        print(f"end processing query {end-start}")
        relevant_documents = []

        for i in range(len(vector)):
            if vector[i] == 1:
                relevant_documents.append(self.collection[i])

        return relevant_documents




 

   
 
def start(collection, irm, query):

    collections = {'newsgroup': lambda d : Newsgroups(d)}
    irms = {'boolean': lambda c,t,q : BooleanIRM(c,t,q)}

    query = (re.sub(r'[^\w\s]', ' ', query.lower())).split(' ')

    col, terms = collections[collection](DIR).parse()

    model = irms[irm](col,terms,query)

    return model.retrieve_documents()

  

       

#print("Write a query: ")
#query=input()
#start('newsgroup','boolean', query)


dic ={'key':'value'}
print(dic.get('key'))
v = dic.get('key')
v = 'hola'
dic.update({'key':v})
print(dic.get('key'))
dic.update({'l':'m'})
print(len(dic))
print(v.count)
start=time.time()
#c = Cranfield("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\cran\\cran.all.1400")  
#c=Cranfield("C:\\Users\\Marie\\Desktop\\New folder\\New Text Document.txt")
#for d in os.scandir("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\cran"):
#    print(d)
#a,b=c.parse()
n = Newsgroups("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\20 Newsgroups\\20news-18828")
d,c=n.parse()
print(d)
end = time.time()
print(end-start)


    

    


  
        
        