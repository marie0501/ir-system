import glob
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
from collections import Counter
import numpy as np
from collections import OrderedDict

#NOTA: Creo que este metodo lo tienen de alguna manera en el modelo booleano
# Input: Diccionario de documentos
# Output: Se eliminan las palabras vacías, signos de puntuación y se devuelven todas las palabras
# de la collección en una lista
def wordList(doc_dict):
    stop = stopwords.words('english') + list(string.punctuation) + ['\n']
    wordList = []
    for doc in doc_dict.values():
        for word in word_tokenize(doc.lower().strip()): 
            if not word in stop:
                wordList.append(word)
    return wordList

#Input: Vocabulario de las palabras y diccionario de documentos
#Output: Diccionario de diccionarios que relaciona en cada documetnto, cada palabra con su tf
def tF_Doc(vocab, doc_dict):
    tf_docs = {}
    for doc_id in doc_dict.keys():
        tf_docs[doc_id] = {}
    
    for word in vocab:
        for doc_id,doc in doc_dict.items():
            tf_docs[doc_id][word] = doc.count(word)
    return tf_docs

#Input: Vocabulario de las palabras y el dicionario de documentos
#Output: Diccionario donde cada palabra se relaciona con su frecuencia
def wordDocFrecuency(vocabulary, doc_dictionary):
    df = {}
    for word in vocabulary:
        freq = 0
        for doc in doc_dictionary.values():
            if word in word_tokenize(doc.lower().strip()):
                freq = freq + 1
        df[word] = freq
    return df

#Input: Vocabulario, diccionario de frecuencia de documetnos y cantidad de documentos
#Output: diccionario con idf del documento
def inverseDocFrecuency(vocabulary,doc_frecuency,length):
    idf= {} 
    for word in vocabulary:     
        idf[word] = np.log2((length+1) / doc_frecuency[word])
    return idf
#Input:
# Vocabulario
# tf
# idf
# documentos
#Output: diccionario con el valor de tf*idf asociado a cada palabra
def tf_idf(vocabulary,tf,idf_scr,doc_dictionary):
    tf_idf_scr = {}
    for doc_id in doc_dictionary.keys():
        tf_idf_scr[doc_id] = {}
    for word in vocabulary:
        for doc_id,doc in doc_dictionary.items():
            tf_idf_scr[doc_id][word] = tf[doc_id][word] * idf_scr[word]
    return tf_idf_scr

#Input: Consulta, dicccionario de documentos y diccionario de tf*idf 
def vectorSpaceModel(query, doc_dict,tf_idf_scr):
    query_vocab = []
    for word in query.split():
        if word not in query_vocab:
            query_vocab.append(word)

    query_wc = {}
    for word in query_vocab:
        query_wc[word] = query.lower().split().count(word)
    
    relevance_scores = {}
    for doc_id in doc_dict.keys():
        score = 0
        for word in query_vocab:
            score += query_wc[word] * tf_idf_scr[doc_id][word]
        relevance_scores[doc_id] = score
    sorted_value = OrderedDict(sorted(relevance_scores.items(), key=lambda x: x[1], reverse = True))
    top_5 = {k: sorted_value[k] for k in list(sorted_value)[:5]}
    return top_5

#Debemos unirlo al primer .py o separar el analisis de los documentos para usarlo
#    w_List = wordList(docs)           #returns a list of tokenized words
#    vocab = list(set(w_List))         #returns a list of unique words
#    tf_dict = tF_Doc(vocab, docs)     #returns term frequency
#    df_dict = wordDocFrecuency(vocab, docs)             #returns document frequencies
#    idf_dict = inverseDocFrecuency(vocab,df_dict,M)     #returns idf scores
#    _tf_idf = tf_idf(vocab,tf_dict,idf_dict,docs)   #returns tf-idf socres
   