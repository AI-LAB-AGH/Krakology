from sklearn.preprocessing import MinMaxScaler
from typing import Tuple

import pandas as pd
import torch


def normalize_numeric(data: pd.DataFrame, min: int = 0, max: int = 0):
    pass


def create_sequences(data: pd.DataFrame, seq_length: int, target_name: str, prediction_horizon: int) -> Tuple[torch.Tensor, torch.Tensor]:
    '''
    Returns a pair: (feature_sequences, target_sequences) of torch tensors
    '''

    sequences = []
    targets = []

    for i in range(len(data) - seq_length):
        seq = data.iloc[i:i + seq_length].drop(columns=[target_name]).values
        sequences.append(seq)

        tgt = data.iloc[i + seq_length:i + seq_length + prediction_horizon][target_name]
        targets.append(tgt)

    return torch.tensor(sequences), torch.tensor(targets)
