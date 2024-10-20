import csv
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from forecasting.inference import predict_poland

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


def process_events(data, start_date, end_date, days_to_extrapolate):
    data['data'] = pd.to_datetime(data['date'], format='%d.%m.%Y')

    data = data.drop('city')
    data = data.drop('event_ID')

    data_weak = data.drop('is_event')
    data_weak = data_weak.drop('min_people')
    data_weak = data_weak.drop('max_people')

    data_train = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    data_test = data[(data['date'] > end_date) & (data['date'] <= end_date + pd.Timedelta(days=days_to_extrapolate))]

    data_weak_train = data_weak[(data_weak['date'] >= start_date) & (data_weak['date'] <= end_date)]
    data_weak_test = data_weak[(data_weak['date'] > end_date) & (data_weak['date'] <= end_date + pd.Timedelta(days=days_to_extrapolate))]

    X_train, X_test, y_train, y_test = data_train.loc[:, data_train.columns != 'quantity'].values, data_test.loc[:, data_test.columns != 'quantity'].values, data_train['quantity'].to_numpy(), data_test['quantity'].to_numpy()
    X_weak_train, X_weak_test, y_weak_train, y_weak_test = data_weak_train.loc[:, data_weak_train.columns != 'quantity'].values, data_weak_test.loc[:, data_weak_test.columns != 'quantity'].values, data_weak_train['quantity'].to_numpy(), data_weak_test['quantity'].to_numpy()

    y_pred_weak = predict_poland(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
    y_pred = predict_poland(X_train=X_weak_train, X_test=X_weak_test, y_train=y_weak_train, y_test=y_weak_test)

    data_weak = data + y_pred_weak
    data_good = data + y_pred

    data_weak = select_top_5(data_weak)
    data_good = select_top_5(data_good)

    return data_weak, data_good


def select_top_5(data):
    data = sorted(data, lambda x: (np.max(x[:, 1]) - np.min(x[:, 0]) / np.min(x[:, 0])))
    return data[:5]


def generate_graph(data):
    pass