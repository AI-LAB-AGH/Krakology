from sklearn.preprocessing import MinMaxScaler
from typing import Tuple

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


def create_sequences(data: pd.DataFrame, seq_length: int, target_name: str, prediction_horizon: int) -> Tuple[torch.Tensor, torch.Tensor]:
    '''
    Returns a pair: (feature_sequences, target_sequences) of torch tensors
    '''

    sequences = []
    targets = []

    data = data.drop(columns=['date'])

    for i in range(len(data) - seq_length - prediction_horizon):
        seq = data.iloc[i:i + seq_length].drop(columns=[target_name]).values
        sequences.append(seq)

        tgt = data.iloc[i + seq_length:i + seq_length + prediction_horizon][target_name]
        targets.append(tgt)

    return torch.tensor(sequences), torch.tensor([t.to_numpy() for t in targets])
