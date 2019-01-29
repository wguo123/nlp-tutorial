import torch
import torch.nn as nn
import torch.nn.functional as F

class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Encoder, self).__init__()
        
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(input_size, hidden_size) 
        # |input_size| = (input_lang.n_words)
        self.gru = nn.GRU(hidden_size, hidden_size)

    def forward(self, input, hidden):
        # |input|, |hidden| = (1), (1, 1, hidden_size)
        embedded = self.embedding(input).view(1,1,-1)
        output = embedded
        # |output|, |embedded| = (1, 1, hidden_size)
        output, hidden = self.gru(output, hidden)
        # |output|, |hidden| = (1, 1, hidden_size)
        return output, hidden
    
    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size)

class Decoder(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(Decoder, self).__init__()
        
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(output_size, hidden_size)
        # |output_size| = (output_lang.n_words)
        self.gru = nn.GRU(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        # |input|, |hidden| = (1), (1, 1, hidden_size)
        output = self.embedding(input).view(1,1,-1)
        output = F.relu(output)
        # |output| = (1, 1, hidden_size)
        output, hidden = self.gru(output, hidden)
        # |output|, |hidden| = (1, 1, hidden_size)
        # |output[0]| = (1, hidden_size)
        output = self.softmax(self.out(output[0]))
        # |output| = (1, output_lang.n_words)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1,self.hidden_size)

