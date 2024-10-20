import numpy as np
import pandas as pd
import plotly as ply
import plotly.graph_objects as go
from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from forecasting.inference import predict_poland, create_lag_features


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
    with open('./backend/past.csv', 'w') as f:
        f.write("date,unit_sales\n")
        for idx, row in sales_data.iterrows():
            f.write(f"{row['date']},{row['quantity']}\n")

    data_weak, data_good = process_events(sales_data)

    for idx in sales_data[sales_data['event_ID'] != -1]['event_ID'].unique():
        event = events_data[int(idx)]
        event['description'] = 'None'
        events.append(event)

    generatePlot('./backend/past.csv', './backend/predictions.csv')
    return JsonResponse({"events": events})


def process_events(data, start_date, end_date, days_to_extrapolate):
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')

    data = create_lag_features(data, column='quantity', lags=5)

    data = data.drop(columns=['city'])
    data = data.drop(columns=['event_ID'])

    data_weak = data.drop(columns=['is_event'])
    data_weak = data_weak.drop(columns=['min_people'])
    data_weak = data_weak.drop(columns=['max_people'])

    data_train = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    data_test = data[(data['date'] > end_date) & (data['date'] <= end_date + pd.Timedelta(days=days_to_extrapolate))]

    data_weak_train = data_weak[(data_weak['date'] >= start_date) & (data_weak['date'] <= end_date)]
    data_weak_test = data_weak[(data_weak['date'] > end_date) & (data_weak['date'] <= end_date + pd.Timedelta(days=days_to_extrapolate))]

    y_pred_weak = predict_poland(data_weak_train, data_weak_test)
    y_pred = predict_poland(data_train, data_test)

    print(y_pred[0])
    print(len(y_pred[1]))

    data_weak = select_top_5(y_pred_weak)
    data_good = select_top_5(y_pred)

    for i in range(5):
        date_range_extrapolated = pd.date_range(start=end_date + pd.Timedelta(days=1), end=end_date + pd.Timedelta(days=days_to_extrapolate))
        date_list_extrapolated = date_range_extrapolated.strftime('%d.%m.%Y').tolist()

        csv_contents = zip(date_list_extrapolated, data_weak[i][1], data_good[i][1])
        
        with open(f'backend/predictions_{i}.csv', 'w') as f:
            f.write('date,unit_sales_x,unit_sales_y\n')

            for line in csv_contents:
                f.write(f'{line[0]},{line[1]},{line[2]}\n')


def select_top_5(data):
    data = sorted(data, key=lambda x: max(x[1]))
    return data[:5]


def plotGiven(name,title,past_p,avaliable,*args):
    show_vec=[past_p]
    for ix, val in enumerate(args):
        if val==1: 
            show_vec.append(avaliable[ix])
    fig = go.Figure(data=show_vec)
    fig.update_layout(
    title=title,
    xaxis_title='Date',
    yaxis_title='Sold items')
    fig.update_layout(title=dict(font=dict(size=40),xanchor='center'),title_x=0.5,font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    ))
    fig.show()
    fig.write_html(name)


def generatePlot( past_csv, predictions_csv, future_csv=False, show=[1,1,1], name="plot.html",title='Predicted sale'):
    past = pd.read_csv(past_csv)
    preds = pd.read_csv(predictions_csv)
        
    pred1_p = go.Scatter(x=preds['date'], y=preds['unit_sales_x'], mode='lines', name='Predykcja modelu 1', line=dict(color="#1e6abf"),
                        hovertemplate='<b>Date:</b> %{x}<br><b>Sold Items:</b> %{y}<extra></extra>')
    pred2_p = go.Scatter(x=preds['date'], y=preds['unit_sales_y'], mode='lines', name='Predykcja modelu 2', line=dict(color="#ac1ebf"),
                        hovertemplate='<b>Date:</b> %{x}<br><b>Sold Items:</b> %{y}<extra></extra>')
    past_p = go.Scatter(x=past['date'], y=past['unit_sales'], mode='lines', name='Przeszłość', line=dict(color="#19ae55"),
                       hovertemplate='<b>Date:</b> %{x}<br><b>Sold Items:</b> %{y}<extra></extra>')

    if (future_csv is not False): 
        future_t = pd.read_csv(future_csv)
        future_p = go.Scatter(x=future_t['date'], y=future_t['unit_sales'], mode='lines', name='Faktyczne wyniki', line=dict(color="#aedf2b"))
        plotGiven(name,title,past_p,[pred1_p,pred2_p,future_p],*show)
    else: 
        show[2]=0
        plotGiven(name,title,past_p,[pred1_p,pred2_p,0],*show)