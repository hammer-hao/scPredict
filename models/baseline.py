import torch.nn as nn
from settings import *
import torch

class MLPClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.ffwd = nn.Sequential(
            nn.BatchNorm1d(79),
            nn.Linear(79, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.ffwd(x)
    

def concatenate_rows_single_last_column(tensor):
    sorted_tensor, indices = torch.sort(tensor, dim=0, descending=False)
    last_col_vals = sorted_tensor[:, -1]
    unique_vals, counts = torch.unique(last_col_vals, return_counts=True)
    paired_indices = unique_vals[counts == 2]
    mask = torch.isin(last_col_vals, paired_indices)
    to_concatenate = sorted_tensor[mask]
    to_concatenate = to_concatenate.view(-1, 2, to_concatenate.size(1))
    concatenated = torch.cat((to_concatenate[:, 0, :-1], to_concatenate[:, 1, :]), dim=1)
    return concatenated