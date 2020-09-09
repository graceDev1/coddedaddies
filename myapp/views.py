from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from .models import Search
# Create your views here.

base_url = "https://losangeles.craigslist.org/search/?query={}"
def home(request):
    context = {}
    return render(request, 'home.html', context)


def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = base_url.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    # post_title = post_listings[0].find(class_ = 'result-title').text
    # post_url = post_listings[0].find('a').get('href')
    # post_price = post_listings[0].find(class_ = 'result-price').text
    # print(post_price)

   
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_="result-title").text
        post_url = post.find('a').get('href')
        post_price = post.find(class_="result-price").text
        final_postings.append((post_title, post_url, post_price))
        if post.find(class_='result-price'):
            post_price = post.find(class_ = 'result-price').text
        else:
            post_price = 'N/A'
        BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)
        
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_postings.append((post_title, post_url, post_price,post_image_url))
  
    context = {
        "search_res": search,
        "final_postings":final_postings
    }
    # print(final_url)
    return render(request, 'my_apps/new_search.html', context)
