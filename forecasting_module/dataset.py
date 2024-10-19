from torch.utils.data import Dataset

class SalesDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    
    def __len__(self):
        return len(self.X)

    def __repr__(self) -> str:
        return "Class to load custom data from local source"
    
    def __getitem__(self, idx) -> None:
        return self.X[idx], self.y[idx]

