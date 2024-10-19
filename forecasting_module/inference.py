import pandas as pd

from preprocessing import create_lag_features
from trees import train

def predict_equador(item, city, state):
    df = pd.read_csv('data/data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    data = df

    data = data.loc[data['family'] == item]
    data = data.loc[data['city'] == city]
    data = data.loc[data['state'] == state]

    dates = data['date'].values
    data = data.drop(columns=['date'])
    data = data.drop(columns=['family'])
    data = data.drop(columns=['city'])
    data = data.drop(columns=['state'])

    data = create_lag_features(data, column='unit_sales', lags=10)

    X, y = data.loc[:, data.columns != 'unit_sales'].values, data['unit_sales'].to_numpy()

    print(X.shape)

    split = int(0.8 * len(X))

    X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

    train(X_train, X_test, y_train, y_test)
