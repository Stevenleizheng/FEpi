import esm
import torch
import torch.nn as nn
import torch.nn.functional as F


class EnzymeBinary(nn.Module):
    """binary classification model"""
    def __init__(self, n_class):
        super(EnzymeBinary, self).__init__()
        self.esm = esm.pretrained.esm2_t33_650M_UR50D()[0]
        for name, param in self.named_parameters():
            param.requires_grad =False
        self.fc1 = nn.Linear(1280, 960)
        self.fc2 = nn.Linear(960, 480)
        self.fc3 = nn.Linear(480, 120)
        self.fc4 = nn.Linear(120, n_class)
    def forward(self, batch_tokens):
        x = self.esm(batch_tokens, repr_layers=[33], return_contacts=False)["representations"][33]
        batch_tokens = batch_tokens.unsqueeze(-1)
        x = x.masked_fill(batch_tokens<=2, 0)
        num = torch.sum(batch_tokens>2, axis=1)
        x = x.sum(axis=1) / num
        res = []
        res.append(x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)   
        res.append(x)    
        return res

