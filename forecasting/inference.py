import pandas as pd

from .preprocessing import create_lag_features
from .trees import train


def predict_equador(item):
    df = pd.read_csv('data/equador.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df = df.loc[df['family'] == item]
    dates = df['date'].values
    df = df.drop(columns=['date'])
    df = df.drop(columns=['family'])

    for state in df['state'].unique():
        df = df.loc[df['state'] == state]
        for city in df['city'].unique():
            df = df.loc[df['city'] == city]
            data = df.drop(columns=['state'])
            data = data.drop(columns=['city'])

            data = create_lag_features(data, column='unit_sales', lags=10)

            X, y = data.loc[:, data.columns != 'unit_sales'].values, data['unit_sales'].to_numpy()

            split = int(0.8 * len(X))

            X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

            y_pred = train(X_train, X_test, y_train, y_test)


def predict_poland(data_train, data_test, lag=10):
    X_train = data_train
    X_test = data_test

    X_train = X_train.drop(columns=['date'])
    X_test = X_test.drop(columns=['date'])

    preds = []

    for x in X_train['store_localisation_x'].unique():
        X_train_ = X_train.loc[X_train['store_localisation_x'] == x]
        X_train_ = X_train_.drop(columns=['store_localisation_x'])
        X_train_ = X_train_.drop(columns=['store_localisation_y'])
        X_train_ = X_train_.drop(columns=['product'])

        for idx, row in X_train_.iterrows():
            id = row['store_id']
            break

        if 'is_event' in X_train_.columns:
            X_train_ = create_lag_features(X_train_, column='is_event')

        if 'min_people' in X_train_.columns:
            X_train_ = create_lag_features(X_train_, column='min_people')
        
        if 'max_people' in X_train_.columns:
            X_train_ = create_lag_features(X_train_, column='max_people')

        X_test_ = X_test.loc[X_test['store_localisation_x'] == x]
        X_test_ = X_test_.drop(columns=['store_localisation_x'])
        X_test_ = X_test_.drop(columns=['store_localisation_y'])
        X_test_ = X_test_.drop(columns=['product'])

        if 'is_event' in X_test_.columns:
            X_test_ = create_lag_features(X_test_, column='is_event')
        
        if 'min_people' in X_test_.columns:
            X_test_ = create_lag_features(X_test_, column='min_people')
        
        if 'max_people' in X_test_.columns:
            X_test_ = create_lag_features(X_test_, column='max_people')

        X_train_, X_test_, y_train_, y_test_ = X_train_.loc[:, X_train_.columns != 'quantity'].values, X_test_.loc[:, X_test_.columns != 'quantity'].values, X_train_['quantity'].to_numpy(), X_test_['quantity'].to_numpy()

        y_pred = train(X_train_, X_test_, y_train_, y_test_)
        preds.append([id, y_pred])

    return preds
