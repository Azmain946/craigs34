from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models
# Create your views here.

BASE_CRAIGLISTS_URL = 'https://cambridge.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
import requests

proxies={
    'https':'51.158.68.68:8811',
    'http':'51.158.68.68:8811',
}




def home(request):
    return render(request, template_name='base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGLISTS_URL.format(str(quote_plus(str(search))))
    print(final_url)
    response = requests.get(final_url,proxies=proxies)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post = soup.find_all('li',{'class':'result-row'})
    final_posting=[]
    for p in post:
        post_title = p.find(class_='result-title').text


        post_url = p.find('a').get('href')
        post_price = "N/A"
        if p.find(class_='result-price'):
            post_price = p.find(class_='result-price').text
        image_url="https://craigslist.org/images/peace.jpg"
        if p.find(class_='result-image').get('data-ids'):
            post_image = p.find(class_='result-image').get('data-ids').split(',')[0].split(":")[1]
            image_url = BASE_IMAGE_URL.format(post_image)

        final_posting.append((post_title,post_url,post_price,image_url))

    #print(post_title)
    stuff_for_frontend = {
        'search': search,
        'final_posting':final_posting,
    }
    return render(request,'my_app/new_search.html',stuff_for_frontend)