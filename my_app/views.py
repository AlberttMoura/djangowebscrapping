from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}&sort=rel'

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search').lower() .strip()
    models.Search.objects.create(search=search)
    search_url = ( '+'.join(search.split()))
    final_url = BASE_CRAIGSLIST_URL.format(search_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_titles = soup.find_all('a', {'class': 'result-title'})
    context = {
        'search' : search,
        'final_posting' : [],
    }
    return render(request, 'my_app/new_search.html', context)
