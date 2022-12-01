from django.shortcuts import render, redirect
import main
import pickle


# Create your views here.
def index(request):

    if request.method == 'POST':
        query = request.POST['query']
        collection = request.POST.get('collection')  
        irm = request.POST.get('irm')

        retrieved_documents_file = main.retrieve(query,collection,irm)        
        
        return redirect('results', documents_file=retrieved_documents_file)        

    return render(request,'index.html')

def results(request, documents_file):

    if request.method == 'POST':
        query = request.POST['query']
        collection = request.POST.get('collection')  
        irm = request.POST.get('irm')
        documents_file = main.retrieve(query,collection,irm) 

    with open(documents_file,'rb') as f:
        documents = pickle.load(f)

    return render(request, 'results.html',{'documents':documents})