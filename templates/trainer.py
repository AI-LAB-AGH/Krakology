from torch import nn
from tqdm import tqdm
from torch.optim import AdamW

import torch


class MyTrainer():
    def __init__(self) -> None:
        self.optimizer = None
        self.loss = None
        self.batch_size = None

    def __repr__(self) -> str:
        return "Klasa do trenowania modelu, zbiera w sobie dataloader, dataset, model"
    
    def train(self):
        "Tu będzie trenowanie modelu -> pętla po epokach, batchach, itd."
        return

def train(self, model: nn.Module, dataloader: torch.utils.data.DataLoader, n_epochs: int, lr: float = 0.001):
    optimizer = AdamW(model.parameters(), lr=lr)
    loss = nn.MSELoss()

    model.train()

    for epoch in range(n_epochs):
        epoch_loss = 0

        for X_batch, y_batch in tqdm(dataloader, desc=f'Epoch {epoch}, loss: {epoch_loss}'):
            optimizer.zero_grad()
            y_pred = model(X_batch)
            loss = loss(y_pred, y_batch)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
