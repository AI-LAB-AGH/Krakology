import torch
from torch import nn

class LSTMForecaster(nn.Module):
    def __init__(self, input_size, hidden_dim, num_layers, output_size, output_steps = 7):
        super(LSTMForecaster, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_size)
        self.h = None
        self.c = None
        self.num_layers = num_layers
        self.hidden_dim = hidden_dim
        self.output_steps = output_steps

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))
        out = self.fc(out[:, -self.output_steps:, :]) 
        return out
