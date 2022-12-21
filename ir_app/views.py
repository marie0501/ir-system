from django.shortcuts import render, redirect
import main
import pickle


# Create your views here.
def index(request):
    
    if request.method == 'POST':
        query = request.POST['query']
        collection = request.POST.get('collection')  
        irm = request.POST.get('irm')
        main.retrieve(query,collection,irm)        
        
        return redirect('results')        

    return render(request,'index.html')

def results(request):
    
    if request.method == 'POST':
        query = request.POST['query']
        collection = request.POST.get('collection')  
        irm = request.POST.get('irm')
        main.retrieve(query,collection,irm) 
        
    with open('retrieved_documents','rb') as f:
        documents = pickle.load(f)
    
           
    return render(request, 'results.html',{'documents':documents, 'length':len(documents)})

def document(request, id):    
    
    with open('retrieved_documents','rb') as f:
        documents = pickle.load(f)
    
    selected_doc = None
    for doc in documents:
        if doc.id == id:
            selected_doc = doc
            break
        
    
    return render(request,'document.html',{'document':selected_doc})

    
    
    