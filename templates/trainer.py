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

def train(model: nn.Module, dataloader: torch.utils.data.DataLoader, test_loader, optimizer, criterion, n_epochs: int, lr: float = 0.001):
    model.train()

    for epoch in range(n_epochs):
        epoch_loss = 0

        for X_batch, y_batch in tqdm(dataloader, desc=f'Epoch {epoch}'):
            optimizer.zero_grad()
            y_pred = model(X_batch)
            y_pred = torch.squeeze(y_pred)
            loss = criterion(y_pred, y_batch)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        epoch_loss /= len(dataloader)
        test_loss = test(model, test_loader)
        print(f'Epoch {epoch} | train_loss: {epoch_loss} | test_loss: {test_loss}')


def test(model: torch.nn.Module, dataloader: torch.utils.data.DataLoader):
    model.eval()

    criterion = torch.nn.MSELoss()
    test_loss = 0.0

    with torch.no_grad():
        for X_batch, y_batch in tqdm(dataloader, desc="Evaluating"):
            y_pred = model(X_batch)
            y_pred = torch.squeeze(y_pred)
            loss = criterion(y_pred, y_batch)
            test_loss += loss.item()
    avg_test_loss = test_loss / len(dataloader)

    return avg_test_loss
