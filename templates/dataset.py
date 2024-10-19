from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    
    def __len__(self):
        return self.X.size[0]

    def __repr__(self) -> str:
        return "Class to load custom data from local source"
    
    def __getitem__(self, idx) -> None:
        return self.X[idx], self.y[idx]

