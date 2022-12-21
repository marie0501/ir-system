
import numpy as np
from numpy.linalg import svd
from scipy.sparse.linalg import svds
import math
import re
import json



operators = {
    'and' : lambda x,y : op_and(x,y),
    'or' : lambda x,y : op_or(x,y),
    'not' : lambda x : op_not(x)
}

def precedence(op):
     
    if op == 'or':
        return 1
    elif op == 'and':
        return 2
    elif op == 'not':
        return 3
    
    return 0

def op_or(x,y):
    vector_result=[]
    for i in range(len(x)):
                if x[i] == 0 and y[i] == 0:
                    vector_result.append(0)
                else:
                    vector_result.append(1)

    return vector_result

def op_and(x,y):
    vector_result=[]
    for i in range(len(x)):
                if x[i] > 0 and y[i] > 0:
                    vector_result.append(1)
                else:
                    vector_result.append(0)
    return vector_result

def op_not(x):
    vector_result=[]
    for i in x:
                if i > 0:
                    vector_result.append(0)
                else:
                    vector_result.append(1)
    return vector_result
 
 
# Function that returns value of
# expression after evaluation.
def evaluate(tokens):
     
    # stack to store integer values.
    values = []
     
    # stack to store operators.
    ops = []
    i = 0

    try:
     
        while i < len(tokens):       

            # Current token is an opening
            # brace, push it to 'ops'
            if tokens[i] == '(':
                ops.append(tokens[i])

            elif tokens[i] not in set(operators.keys()) and tokens[i]!=')':
                values.append(dic[tokens[i]])

            # Closing brace encountered,
            # solve entire brace.
            elif tokens[i] == ')':
            
                while len(ops) >0 and ops[-1] != '(':
                
                    op = ops.pop()

                    if op == 'not':
                        val1 = values.pop()
                        values.append(operators[op](val1))
                    else:
                        val2 = values.pop()
                        val1 = values.pop()
                        values.append(operators[op](val1, val2))

                # pop opening brace.
                ops.pop() 

                if len(ops)>0 and ops[-1]=='not':
                    op =ops.pop()
                    val1 = values.pop()
                    values.append(operators[op](val1))   

            #elif tokens[i] == 'not':
            #    if (i < (len(tokens) - 1)) and (tokens[i+1] not in set(operators.keys())) and (tokens[i+1] !='(') and (tokens[i+1] != ')'):
            #        val1 = dic[tokens[i+1]]
            #        values.append(operators['not'](val1))
            #        i+=1

            # Current token is an operator.
            elif tokens[i] in set(operators.keys()):

                while (len(ops) != 0 and
                    precedence(ops[-1]) >=
                       precedence(tokens[i])):

                    op = ops.pop()

                    if op == 'not':
                        val1 = values.pop()
                        values.append(operators[op](val1))
                    else:
                        val2 = values.pop()
                        val1 = values.pop()
                        values.append(operators[op](val1, val2))

                # Push current token to 'ops'.
                ops.append(tokens[i])



            i += 1

        # Entire expression has been parsed
        # at this point, apply remaining ops
        # to remaining values.
        while len(ops) != 0:

            op = ops.pop()

            if op == 'not':
                val1 = values.pop()
                values.append(operators[op](val1))
            else:
                val2 = values.pop()
                val1 = values.pop()
                values.append(operators[op](val1, val2))

        # Top of 'values' contains result,
        # return it.
        return values[-1]

    except:
        print('Invalid query')
        
 

     
dic = {
    'stream':[0,1,1,0],
    'layer':[1,1,0,0],
    'aerodynamics':[1,0,1,0],
    'hola':[0,0,0,1]
}
#query = '(stream and layer) or aerodynamics.'
#tokens =['not','(','not','hola','and','not','(','stream', 'and','layer',')','or','not','aerodynamics']
#print(evaluate(tokens))
#
#print('hola' in dic.keys())
#print(dic.keys()[0])
#
#a = np.array([[1,2,3],[4,5,6]])
#print(a.shape[0])



a = np.array([[1,2,3], [4,5,6], [7,8,9], [10,11,12]], dtype=float)
print(a.shape)
print(a)
U,S,V = svd(a)#,k=2,which='LM')
#U=np.round(U,4)
#S=np.round(S,4)
#V=np.round(V,4)
#print(U.shape)
#print(S.shape)
#print(V.shape)
#print(U)
#print(S)
#print(V)
#sigma = np.zeros((3,3))
#for i in range(3):
#    sigma[i,i] = S[i]
#
#print(sigma)
#print(sigma.shape)
#

#print(U_red)
#n = np.empty((1,3))
#v = np.transpose(np.vstack(V[1,:]))
#u = np.vstack(U_red[:,1])
#print(u)
#print(v)
#print(v.shape)
#print(u.shape)
#print(np.matmul(u,v))

b = np.empty((4,3))
for i in range(3):
  b += np.array(int(np.sqrt(S[i]))*np.matmul(np.vstack(U[:,i]),np.transpose(np.vstack(V[i,:]))),dtype='int32')
print(0.00000000000000000000000001 > 10e-16)
c =[1,2,3,4]
d=np.delete(c,0)
e = np.divide(d, [1,2,3])
print(e)

print('---------------------')
    
index = r'[1-9]* [1-9]*'



s ='200 1300'

m=re.match(index,s)
print(re.match(index,s))
#print(m.group().split()[1])

dic ={'hol':2,'l':1,'k':5}
print(dic.keys())
print(set(dic.keys()))
print(dic['hol'])

f =np.array([[1,2,3],[4,5,6]])
e=[1,2,3]
print(np.dot(e,e))
c = f[:,1]
d=[1,2]
print(c)
print(np.matmul(c,d))
print(np.linalg.norm(e))

r=dict(sorted(dic.items(), key = lambda item: item[1], reverse=True))



r = r'.*'
d = '"Hola mi nombre es, Marie"'
l=d.removeprefix('"').removesuffix('"')
print(l)

for w.casefold() in d:
    
