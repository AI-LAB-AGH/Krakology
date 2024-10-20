import pandas as pd

from preprocessing import create_lag_features
from trees import train


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


def predict_poland(item):
    df = pd.read_csv('data/equador.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df = df.loc[df['family'] == item]
    dates = df['date'].values
    df = df.drop(columns=['date'])
    df = df.drop(columns=['family'])

    for x in df['store_localisation_x'].unique():
        df = df.loc[df['store_localisation_x'] == x]
        data = df.drop(columns=['store_localisation_x'])
        data = data.drop(columns=['store_localisation_y'])

        data = create_lag_features(data, column='unit_sales', lags=10)

        X, y = data.loc[:, data.columns != 'unit_sales'].values, data['unit_sales'].to_numpy()

        split = int(0.8 * len(X))

        X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

        y_pred = train(X_train, X_test, y_train, y_test)
