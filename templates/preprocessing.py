from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from typing import Tuple, List

import pandas as pd
import torch


def normalize_numeric_minmax(data: pd.DataFrame, range_min: int = 0, range_max: int = 1) -> pd.DataFrame:
    '''
    Automatically detects numeric columns and minmax normalizes them
    '''
    scaler = MinMaxScaler(feature_range=(range_min, range_max))
    numeric_columns = data.select_dtypes(include=['float64']).columns
    data[numeric_columns] = scaler.fit_transform(data[numeric_columns])
    return data


def create_sequences(data: pd.DataFrame, seq_length: int, target_name: str, prediction_horizon: int, item_column: str='family') -> Tuple[torch.Tensor, torch.Tensor]:
    '''
    Returns a pair: (feature_sequences, target_sequences) of torch tensors
    '''
    sequences = []
    targets = []

    data = data.drop(columns=['date'])

    data = segment_data(data, column_name=item_column)
    data = [data[3]]

    for category in data:
        for i in range(len(category) - seq_length - prediction_horizon):
            seq = category.iloc[i:i + seq_length + prediction_horizon].drop(columns=[target_name]).values
            sequences.append(seq)

            tgt = category.iloc[i + seq_length:i + seq_length + prediction_horizon][target_name]
            targets.append(tgt)

    return torch.tensor(sequences, dtype=torch.float32), torch.tensor([t.to_numpy() for t in targets], dtype=torch.float32)

def segment_data(df: pd.DataFrame, column_name: str) -> List[pd.DataFrame]:
    grouped_dfs = []

    for column in df.columns:
        if column.startswith(column_name) and df[column].nunique() == 2:
            grouped_dfs.append(df[df[column] == 1])
    
    return grouped_dfs

def create_lag_features(data, column, lags=10):
    df = pd.DataFrame(data[column])
    for i in range(1, lags + 1):
        df[f'lag_{i}'] = df[column].shift(i)
    df.dropna(inplace=True)
    return df

def create_tabular_dataset(data, lags=10):
    for column in data.columns:
        data = create_lag_features(data, column=column, lag=10)
    

