from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import time
from sympy.logic import to_dnf
from src.irm import IRM

class Boolean(IRM):
    
    def __init__(self):
        pass
    
    def search(self, query, collection, indexed_terms_name):
        
        indexed_terms = self._load(indexed_terms_name)
        dnf_query = self.__convert_query_dnf(query)
        cf_vectors = self.__process_dnf_query(dnf_query, indexed_terms) 
        relevant_documents = self.__get_relevant_documents(cf_vectors)

        return collection.retrieve_documents(relevant_documents)        


    def __convert_query_dnf(self, query):
        
        stop_words = set(stopwords.words("english"))
        tokenized_query = word_tokenize(re.sub('[^\w ()\[\]]+',' ',query))
        boolean_op ={
            'and': '&',
            'not':'~',
            'or':'|'
            }
        boolean_query=""
        
        for i in range(len(tokenized_query)):
            print(boolean_query)
            if tokenized_query[i] in (boolean_op.keys()-{'not'}):
                boolean_query += f" {boolean_op[tokenized_query[i]]} "
            elif tokenized_query[i]=='not':
                if len(boolean_query)> 0 and boolean_query[len(boolean_query)-1] not in {'&','|','~','('}:
                        boolean_query += ' & '
                boolean_query += boolean_op[tokenized_query[i]]
            elif tokenized_query[i] not in stop_words:
                if len(boolean_query)> 0 and boolean_query[len(boolean_query)-1] not in {'&','|','~','(', ' '} and tokenized_query[i] != ')':
                        boolean_query += ' & '                
                boolean_query += tokenized_query[i]
        print(boolean_query)
                
        return str(to_dnf(boolean_query))       
       

    def __process_dnf_query(self, dnf_query, indexed_terms):

        conjunctive_forms = dnf_query.split('|')
        vector_result = []
        
        for cf in conjunctive_forms:
            vector_result.append(self.__process_conjunctive_form(cf, indexed_terms))
        
        return vector_result


    def __process_conjunctive_form(self, conjuctive_form, indexed_terms):
        
        list_cf = conjuctive_form.replace('(','').replace(')','')
        list_cf = word_tokenize(list_cf)
        print(list_cf)

        bitwise_op = ''
        previous_term_incidence = []
        next_term_incidence = []
        vector_result = []
        has_previous_term = False
        has_not_op = False        

        for term in list_cf:
            if not term in {'&','|','~'}:
                if has_not_op:
                    if has_previous_term:
                        next_term_incidence = self.__process_boolean_op('~', indexed_terms[term], next_term_incidence)
                    else:
                        previous_term_incidence = self.__process_boolean_op('~', indexed_terms[term], next_term_incidence)
                        vector_result = previous_term_incidence

                    has_not_op = False

                elif not(has_previous_term):
                    previous_term_incidence = indexed_terms[term]
                    vector_result = previous_term_incidence
                    has_previous_term = True

                else:
                    next_term_incidence = indexed_terms[term]

            elif term == '~':
                has_not_op = True

            else:              
                bitwise_op = term
            
            if len(next_term_incidence) != 0 and not(has_not_op):
                vector_result = self.__process_boolean_op(bitwise_op, previous_term_incidence, next_term_incidence)
                previous_term_incidence = vector_result
                has_previous_term = True
                next_term_incidence = []

        return vector_result

    def __process_boolean_op(self, bitwise_op, previous_term, next_term):

        vector_result=[]

        if bitwise_op == '~':
            for i in previous_term:
                if i > 0:
                    vector_result.append(0)
                else:
                    vector_result.append(1)

        elif bitwise_op == '&':
            for i in range(len(previous_term)):
                if previous_term[i] > 0 and next_term[i] > 0:
                    vector_result.append(1)
                else:
                    vector_result.append(0)

        elif bitwise_op == '|':
            for i in range(len(previous_term)):
                if previous_term[i] == 0 and next_term[i] == 0:
                    vector_result.append(0)
                else:
                    vector_result.append(1)

        return vector_result

    def __get_relevant_documents(cf_vectors):

        retrieved_documents = {}
        
        for v in cf_vectors:
            for i in range(len(v)-1):
                if v[i] > 0:
                    retrieved_documents.update({i:1})

        return retrieved_documents

    




 

   
 
#def start(collection, irm, query):
#
#    collections = {'newsgroup': lambda d : Newsgroups(d)}
#    irms = {'boolean': lambda c,t,q : Boolean(c,t,q)}
#
#    query = (re.sub(r'[^\w\s]', ' ', query.lower())).split(' ')
#
#    col, terms = collections[collection](DIR).parse()
#
#    model = irms[irm](col,terms,query)
#
#    return model.retrieve_documents()

  

       

#print("Write a query: ")
#query=input()
#start('newsgroup','boolean', query)


#dic ={'key':'value'}
#print(dic.get('key'))
#v = dic.get('key')
#v = 'hola'
#dic.update({'key':v})
#print(dic.get('key'))
#dic.update({'l':'m'})
#print(len(dic))
#print(v.count)
#start=time.time()
##c = Cranfield("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\cran\\cran.all.1400")  
##c=Cranfield("C:\\Users\\Marie\\Desktop\\New folder\\New Text Document.txt")
##for d in os.scandir("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\cran"):
##    print(d)
##a,b=c.parse()
#n = Newsgroups("C:\\Users\\Marie\\Documents\\3er\\S2\\SRI\\Test Collections\\20 Newsgroups\\20news-18828")
#d,c=n.parse()
#print(d)
#end = time.time()
#print(end-start)
#
#

#dic ={'atheist':[0,1,0,1],'religion':[0,0,0,1],'god':[1,1,1,1]} 
#
#print(4 in {1,2,4})
#
#b = Boolean()
#print(b.search("atheist and (religion or god).", [], dic))

    


  
        
        