import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token

def index(request):
    csrf_token = get_token(request)
    return render(request, 'index.html')
    

def scrape_for_events(request):
    # Run scraping script once or twice a day
    print('Scrape success')
    pass


def fetch_events(request):
    data = {
        'id': [1, 2, 3],
        'type': ['KONCERT', 'KATASTROFA', 'EVENT'],
        'scale': ['BIG', 'LARGE', 'SMALL'],
        'start': ['07-01-2005', '07-01-2005', '07-01-2005'],
        'end': ['07-02-2005', '07-02-2005', '07-02-2005'],
        'location': ['KRAKOW', 'KATOWICE', 'WARSZAWA']
    }
    data = pd.DataFrame(data)

    # Fetch events from database
    print('Fetch success')

    data = process_events(data)
    data = data.to_dict(orient='records')
    print('Process success')

    return JsonResponse({"events": data})


def process_events(data):
    # Use model to fit events to client needs and estimate connections between events and products
    return data