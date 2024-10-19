from sklearn.preprocessing import MinMaxScaler
from typing import Tuple

import pandas as pd
import torch


def create_sequences(data: pd.DataFrame, seq_length: int, target_name: str) -> Tuple[torch.Tensor, torch.Tensor]:
    '''
    Returns a pair: (feature_sequences, target_sequences) of torch tensors
    '''

    sequences = []
    targets = []

    for i in range(len(data) - seq_length):
        seq = data.iloc[i:i + seq_length].drop(columns=[target_name]).values
        sequences.append(seq)

        tgt = data.iloc[i:i + seq_length][target_name]
        targets.append(tgt)

    return torch.tensor(sequences), torch.tensor(targets)
