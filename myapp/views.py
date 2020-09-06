from django.shortcuts import render
from bs4 import BeautifulSoup
# Create your views here.

def home(request):
    context = {}
    return render(request, 'home.html', context)


def search(request):
    
    search_res = request.POST['search']
    context = {
        "search_res": search_res
    }
    print(search_res)
    return render(request, 'my_apps/new_search.html', context)
