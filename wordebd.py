import torch.nn as nn
import torch.nn.functional as F
from termcolor import colored


class WORDEBD(nn.Module):
    '''
        An embedding layer that maps the token id into its corresponding word
        embeddings. The word embeddings are kept as fixed once initialized.
    '''
    def __init__(self, vocab, finetune_ebd):#, specific_vocab_size=None):
        super(WORDEBD, self).__init__()

        self.vocab_size, self.embedding_dim = vocab.vectors.size()
        # if specific_vocab_size != None: self.vocab_size = specific_vocab_size
        self.embedding_layer = nn.Embedding(self.vocab_size, self.embedding_dim)
        self.embedding_layer.weight.data = vocab.vectors

        self.finetune_ebd = finetune_ebd

        if self.finetune_ebd:
            self.embedding_layer.weight.requires_grad = True
        else:
            self.embedding_layer.weight.requires_grad = False

    def forward(self, data, weights=None):
        '''
            @param text: batch_size * max_text_len
            @return output: batch_size * max_text_len * embedding_dim
        '''
        if (weights is None) or (self.finetune_ebd == False):
            return self.embedding_layer(data)

        else:
            return F.embedding(data,
                               weights['ebd.embedding_layer.weight'])
