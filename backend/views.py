import csv
import numpy as np
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


def upload_csv(request):
    print(request.FILES.get('csv'))
    return JsonResponse({"data": 0})


def fetch_events(request):
    start_date, end_date, category = request.POST.get('start'), request.POST.get('end'), request.POST.get('category')

    events = []
    events_data = pd.read_csv('./backend/events.csv')
    events_data = events_data.to_dict(orient='records')
    sales_data = pd.read_csv('./backend/sales.csv')

    sales_data = sales_data[sales_data['product'] == category]
    data_weak, data_good = process_events(sales_data)

    for idx in sales_data[sales_data['event_ID'] != -1]['event_ID'].unique():
        event = events_data[int(idx)]
        event['description'] = 'None'
        events.append(event)

    return JsonResponse({"events": events})



    generate_graph(data_weak)
    generate_graph(data_good)


def process_events(data):
    predictions_weak = data.process_weak
    predictions_good = data.process_good

    data_weak = data + predictions_weak
    data_good = data + predictions_good

    data_weak = select_top_5(data_weak)
    data_good = select_top_5(data_good)

    return data_weak, data_good


def select_top_5(data):
    data = sorted(data, lambda x: (np.max(x[:, 1]) - np.min(x[:, 0]) / np.min(x[:, 0])))
    return data[:5]


def generate_graph(data):
    pass